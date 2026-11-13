import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Recipe, ChatLog, Bookmark


def home(request):
    """Main page — show all recipes with search/filter."""
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')

    recipes = Recipe.objects.prefetch_related('ingredients', 'steps').all()

    if q:
        recipes = recipes.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(cuisine__icontains=q) |
            Q(ingredients__name__icontains=q)
        ).distinct()

    if category:
        recipes = recipes.filter(category=category)

    categories = Recipe.objects.values_list('category', flat=True).distinct()

    context = {
        'recipes': recipes,
        'categories': categories,
        'query': q,
        'active_category': category,
        'total_recipes': Recipe.objects.count(),
        'total_chats': ChatLog.objects.count(),
    }
    return render(request, 'recipes/home.html', context)


def recipe_detail(request, pk):
    """Single recipe detail page with cooking mode."""
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related('ingredients', 'steps'), pk=pk
    )
    related = Recipe.objects.filter(
        Q(category=recipe.category) | Q(cuisine=recipe.cuisine)
    ).exclude(pk=pk)[:3]

    return render(request, 'recipes/detail.html', {
        'recipe': recipe,
        'related': related,
    })


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """AI chat endpoint — saves every exchange to ChatLog DB table."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip().lower()
        original = data.get('message', '').strip()
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not message:
        return JsonResponse({'error': 'Empty message'}, status=400)

    # --- Rule-based AI engine ---
    reply, response_type = _generate_reply(message, original)

    # Save to database
    session_key = request.session.session_key or 'anonymous'
    if not request.session.session_key:
        request.session.create()
        session_key = request.session.session_key

    ChatLog.objects.create(
        session_key=session_key,
        user_message=original,
        ai_reply=reply,
        response_type=response_type,
    )

    return JsonResponse({
        'reply': reply,
        'type': response_type,
        'timestamp': __import__('datetime').datetime.now().isoformat(),
    })


def _generate_reply(message, original):
    """Context-aware rule-based AI response engine."""
    keywords = {
        'substitut': ('substitution', "Great substitution question! For butter → use coconut oil or Greek yogurt. For eggs → use 1 tbsp ground flax + 3 tbsp water (flax egg). For cream → coconut milk works perfectly in most savory dishes!"),
        'vegan': ('diet', "For vegan cooking: replace eggs with flax eggs, butter with coconut oil, cream with coconut milk, and meat with chickpeas, lentils, or tofu. The secret is building umami with soy sauce, miso, and nutritional yeast!"),
        'vegetarian': ('diet', "Vegetarian cooking tip: Mushrooms, paneer, lentils, and chickpeas are excellent protein sources. Roasting vegetables at 220°C/425°F caramelises natural sugars and deepens flavour dramatically!"),
        'spicy': ('technique', "To control heat: add chillies whole for mild flavour, sliced for medium, or minced for hot. Remove seeds to reduce spice. Dairy (yogurt, cream) neutralises capsaicin. A pinch of sugar also balances excessive heat!"),
        'storage': ('storage', "Storage tips: Cooked rice → fridge 3-4 days, freeze up to 1 month. Cooked meat → fridge 3-4 days. Fresh herbs → trim stems and store in water like flowers. Avocado → store cut halves with the pit in, sprinkle lemon juice."),
        'marinate': ('technique', "Marinating secrets: Acid (lemon, vinegar, yogurt) tenderises meat — marinate 30 min to 24 hours. Never marinate fish more than 30 minutes (acid cooks it!). Always marinate in the fridge. Pat dry before cooking for a better sear!"),
        'pasta': ('recipe', "Perfect pasta every time: Use 1L salted water per 100g pasta. Cook 1 minute less than the packet says (finish cooking in the sauce!). Reserve 1 cup pasta water — the starchy water emulsifies sauces beautifully!"),
        'rice': ('recipe', "Perfect rice ratio: 1 cup rice → 1.5-2 cups water. Rinse until water runs clear. Bring to boil, then lowest heat for 15 minutes, lid on. Rest 5 minutes without lifting the lid. Fluff with a fork!"),
        'chicken': ('recipe', "Juicy chicken tip: Brine in salted water (1 tbsp salt per cup) for 30 minutes before cooking. Rest for 5 minutes after cooking. Internal temp should reach 75°C/165°F. Thighs are more forgiving than breasts!"),
        'garlic': ('ingredient', "Garlic power tip: Raw garlic has the most punch. Roasting whole bulbs makes it sweet and spreadable. Sautéed garlic (30 seconds) adds aroma. Burnt garlic is bitter — if it burns, start again!"),
        'bake': ('technique', "Baking essentials: Measure by weight, not volume (get a kitchen scale!). Room-temperature butter and eggs are crucial. Don't overmix — it develops gluten and toughens baked goods. Preheat your oven always!"),
        'timer': ('feature', "To use the interactive timer: Click 'Start Cooking' on any recipe card, set your timer for the cooking duration, and it will chime when done! You can also check off ingredients as you prep them."),
        'bookmark': ('feature', "To bookmark a recipe, click the ♡ heart icon on any recipe card. Your bookmarks are saved for your session. You can filter your bookmarked recipes using the top navigation!"),
        'pantry': ('feature', "The Pantry Matcher lets you select ingredients you have at home and finds matching recipes instantly! Click 'Pantry Match' in the navigation and tap the ingredients you have available."),
        'hello': ('greeting', "Hello! 👋 I'm ChefAI, your personal culinary assistant. I can help you with recipes, cooking techniques, ingredient substitutions, storage tips, and much more. What are we cooking today?"),
        'hi': ('greeting', "Hi there! 👋 Welcome to ChefAI! Ask me anything about cooking — techniques, substitutions, nutrition, or just what to make with what you have in the fridge!"),
        'thank': ('gratitude', "You're very welcome! 🍳 Happy cooking! Feel free to ask me anything else — I'm always here to help in the kitchen. Bon appétit!"),
    }

    for kw, (rtype, resp) in keywords.items():
        if kw in message:
            return resp, rtype

    # Try matching a recipe from DB
    try:
        from .models import Recipe as R
        db_match = R.objects.filter(
            Q(title__icontains=original) |
            Q(cuisine__icontains=original) |
            Q(category__icontains=original)
        ).first()
        if db_match:
            return (
                f"I found '{db_match.title}'! It's a {db_match.cuisine} {db_match.category} dish "
                f"taking {db_match.time_minutes} minutes with {db_match.calories} calories. "
                f"{db_match.description[:100]}... You can find it in the recipe list!",
                'recipe_match'
            )
    except Exception:
        pass

    return (
        f"Great culinary question about '{original}'! "
        "The 5 pillars of great cooking are: Salt (season in layers), Fat (flavour carrier), "
        "Acid (brightness — lemon, vinegar), Heat (technique matters!), and Umami (depth — soy, miso, parmesan). "
        "Which aspect would you like to explore?",
        'general'
    )


@csrf_exempt
@require_http_methods(["POST"])
def pantry_match(request):
    """Find recipes matching user's available ingredients."""
    try:
        data = json.loads(request.body)
        ingredients = [i.lower().strip() for i in data.get('ingredients', [])]
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not ingredients:
        return JsonResponse({'recipes': [], 'message': 'No ingredients provided'})

    # Score recipes by ingredient match
    scored = []
    for recipe in Recipe.objects.prefetch_related('ingredients').all():
        recipe_ings = [i.name.lower() for i in recipe.ingredients.all()]
        matches = sum(1 for ing in ingredients if any(ing in ri for ri in recipe_ings))
        if matches > 0:
            scored.append((matches, recipe))

    scored.sort(key=lambda x: -x[0])
    top = scored[:6]

    result = []
    for score, r in top:
        result.append({
            'id': r.pk,
            'title': r.title,
            'category': r.category,
            'cuisine': r.cuisine,
            'time': r.time_minutes,
            'calories': r.calories,
            'image': r.image_url,
            'description': r.description,
            'match_count': score,
        })

    return JsonResponse({'recipes': result})


def api_recipes(request):
    """JSON API endpoint for all recipes."""
    recipes = []
    for r in Recipe.objects.prefetch_related('ingredients', 'steps').all():
        recipes.append({
            'id': r.pk,
            'title': r.title,
            'category': r.category,
            'cuisine': r.cuisine,
            'time': r.time_minutes,
            'difficulty': r.difficulty,
            'calories': r.calories,
            'protein': r.protein,
            'carbs': r.carbs,
            'fat': r.fat,
            'image': r.image_url,
            'description': r.description,
            'ingredients': [i.name for i in r.ingredients.all()],
            'steps': [s.instruction for s in r.steps.all()],
        })
    return JsonResponse({'recipes': recipes, 'count': len(recipes)})
