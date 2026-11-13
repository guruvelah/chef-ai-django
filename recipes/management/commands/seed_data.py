from django.core.management.base import BaseCommand
from recipes.models import Recipe, Ingredient, CookingStep

RECIPES = [
    {
        'title': 'Garlic Butter Tuscan Salmon',
        'category': 'High Protein',
        'cuisine': 'Italian',
        'time_minutes': 25,
        'difficulty': 'Medium',
        'calories': 480,
        'protein': '42g',
        'carbs': '8g',
        'fat': '32g',
        'image_url': 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=800&q=80',
        'description': 'Pan-seared salmon fillets in a luscious sun-dried tomato, spinach, and garlic cream sauce.',
        'ingredients': ['2 fresh salmon fillets (6 oz each)', '2 cloves garlic, minced', '1 cup fresh baby spinach', '1/2 cup heavy cream', '1/3 cup sun-dried tomatoes, drained', '2 tbsp olive oil & 1 tbsp butter', '1/4 cup freshly grated parmesan', 'Salt, pepper & red pepper flakes'],
        'steps': ['Season salmon fillets on both sides with salt, pepper, and a pinch of paprika.', 'Heat olive oil and butter in a large skillet over medium-high heat. Sear salmon skin-side down for 5 minutes until crispy, flip and cook for 3 minutes. Remove to a warm plate.', 'In the same skillet, add minced garlic and sun-dried tomatoes. Saute for 1 minute until fragrant.', 'Reduce heat to medium-low, pour in cream, and bring to a gentle simmer. Stir in parmesan until melted.', 'Fold in fresh spinach until wilted. Return salmon to the skillet and spoon sauce over the fillets.', 'Serve immediately over pasta, rice, or with crusty bread.'],
    },
    {
        'title': 'Spicy Thai Basil Chicken (Pad Krapow)',
        'category': 'Quick',
        'cuisine': 'Asian',
        'time_minutes': 15,
        'difficulty': 'Easy',
        'calories': 380,
        'protein': '35g',
        'carbs': '12g',
        'fat': '18g',
        'image_url': 'https://images.unsplash.com/photo-1562565652-a0d8f0c59eb4?auto=format&fit=crop&w=800&q=80',
        'description': 'Authentic Thai street-food classic - minced chicken stir-fried with Thai basil, fish sauce, and birds-eye chillies.',
        'ingredients': ['400g minced chicken thigh', '1 cup fresh Thai basil leaves', '4 cloves garlic, minced', '3 birds-eye chillies, sliced', '2 tbsp oyster sauce', '1 tbsp fish sauce', '1 tsp soy sauce & 1 tsp sugar', '2 tbsp vegetable oil', '2 fried eggs, to serve'],
        'steps': ['Heat wok over very high heat until smoking. Add oil.', 'Fry garlic and chillies for 30 seconds until fragrant.', 'Add minced chicken, breaking up lumps. Cook 3-4 minutes until no pink remains.', 'Add oyster sauce, fish sauce, soy sauce, and sugar. Toss to combine.', 'Remove from heat and fold in fresh basil leaves.', 'Serve immediately over jasmine rice topped with a crispy fried egg.'],
    },
    {
        'title': 'Creamy Palak Paneer',
        'category': 'Vegetarian',
        'cuisine': 'Indian',
        'time_minutes': 35,
        'difficulty': 'Medium',
        'calories': 320,
        'protein': '18g',
        'carbs': '14g',
        'fat': '22g',
        'image_url': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80',
        'description': 'Vibrant emerald spinach curry with golden paneer cubes in a fragrant spiced tomato-cream gravy.',
        'ingredients': ['250g paneer, cubed', '300g fresh spinach, blanched', '1 large onion, diced', '2 tomatoes, pureed', '1 tbsp ginger-garlic paste', '1 tsp cumin, coriander, garam masala', '1/2 tsp turmeric & chilli powder', '3 tbsp fresh cream', '2 tbsp ghee or butter'],
        'steps': ['Blanch spinach in boiling water for 2 minutes, transfer to ice water. Blend to smooth puree.', 'Pan-fry paneer cubes in 1 tbsp ghee until golden on all sides. Set aside.', 'In the same pan, heat remaining ghee. Add cumin seeds until they splutter.', 'Add onions and cook 8 minutes until golden. Add ginger-garlic paste for 2 minutes.', 'Add tomato puree and all spices. Cook until oil separates (5 minutes).', 'Pour in spinach puree, simmer 5 minutes. Add paneer and cream. Adjust seasoning. Serve with naan.'],
    },
    {
        'title': 'Chocolate Lava Cake',
        'category': 'Dessert',
        'cuisine': 'French',
        'time_minutes': 20,
        'difficulty': 'Medium',
        'calories': 420,
        'protein': '8g',
        'carbs': '45g',
        'fat': '24g',
        'image_url': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=800&q=80',
        'description': 'Decadent individual dark chocolate cakes with a molten liquid centre, served with vanilla ice cream.',
        'ingredients': ['100g dark chocolate (70%), chopped', '100g unsalted butter', '2 whole eggs + 2 egg yolks', '60g caster sugar', '30g plain flour', 'Pinch of salt', 'Cocoa powder for dusting', 'Vanilla ice cream to serve'],
        'steps': ['Preheat oven to 200C/390F. Grease 4 ramekins and dust with cocoa powder.', 'Melt chocolate and butter together in a double boiler. Stir until smooth.', 'Whisk eggs, yolks, and sugar until pale and slightly thickened (about 3 minutes).', 'Fold egg mixture into cooled chocolate. Sift in flour and salt, fold gently.', 'Divide batter into ramekins. Refrigerate up to 24 hours or bake immediately.', 'Bake 10-12 minutes - edges set, centre still jiggles. Rest 1 minute, invert onto plates. Serve at once!'],
    },
    {
        'title': 'Greek Salad with Lemon Herb Chicken',
        'category': 'Low Carb',
        'cuisine': 'Mediterranean',
        'time_minutes': 20,
        'difficulty': 'Easy',
        'calories': 290,
        'protein': '32g',
        'carbs': '10g',
        'fat': '14g',
        'image_url': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=800&q=80',
        'description': 'Bright Mediterranean salad with grilled lemon-herb chicken, kalamata olives, feta, and fresh vegetables.',
        'ingredients': ['2 chicken breasts', '200g cherry tomatoes, halved', '1 cucumber, chopped', '1 red onion, thinly sliced', '100g kalamata olives', '100g feta cheese, crumbled', 'Juice of 2 lemons', '3 tbsp extra virgin olive oil', 'Fresh oregano, salt & pepper'],
        'steps': ['Marinate chicken in lemon juice, 1 tbsp olive oil, oregano, salt, pepper for 15 minutes.', 'Grill chicken on high heat 5-6 minutes per side until cooked through. Rest and slice.', 'Combine tomatoes, cucumber, red onion, and olives in a large bowl.', 'Whisk remaining olive oil with lemon juice, oregano, salt, pepper for dressing.', 'Pour dressing over salad, toss gently. Top with crumbled feta.', 'Arrange sliced chicken over salad. Serve immediately.'],
    },
    {
        'title': 'Classic Beef Burger',
        'category': 'High Protein',
        'cuisine': 'American',
        'time_minutes': 20,
        'difficulty': 'Easy',
        'calories': 650,
        'protein': '45g',
        'carbs': '35g',
        'fat': '38g',
        'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80',
        'description': 'Juicy smash-style beef burger with caramelised onions, melted cheese, and special sauce on a toasted brioche bun.',
        'ingredients': ['500g 80/20 ground beef', '4 brioche buns, toasted', '4 slices American cheese', '1 large onion, thinly sliced', 'Lettuce, tomato slices', '3 tbsp mayo, 1 tbsp mustard, 1 tbsp ketchup', '1 tbsp butter', 'Salt, pepper, garlic powder'],
        'steps': ['Mix mayo, mustard, and ketchup for special sauce. Set aside.', 'Caramelise onions: cook slowly in butter over low heat for 20 minutes.', 'Divide beef into 4 balls. Season generously with salt, pepper, garlic powder.', 'Heat cast iron skillet on high. Place beef ball, smash firmly with spatula. Cook 2 minutes.', 'Flip, immediately top with cheese slice. Cook 1 minute. Build burger.', 'Sauce on both buns, then lettuce, tomato, patty, caramelised onions. Serve immediately.'],
    },
    {
        'title': 'Avocado Toast with Poached Eggs',
        'category': 'Quick',
        'cuisine': 'Mediterranean',
        'time_minutes': 12,
        'difficulty': 'Easy',
        'calories': 340,
        'protein': '16g',
        'carbs': '28g',
        'fat': '20g',
        'image_url': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=800&q=80',
        'description': 'Creamy smashed avocado on sourdough toast topped with perfectly poached eggs and chilli flakes.',
        'ingredients': ['2 ripe avocados', '4 large eggs', '4 slices sourdough bread, toasted', 'Juice of 1 lemon', '1 tbsp white wine vinegar', 'Red chilli flakes & everything bagel seasoning', 'Salt, pepper & micro herbs'],
        'steps': ['Toast sourdough until golden and crispy.', 'Mash avocado with lemon juice, salt, and pepper. Keep slightly chunky.', 'Bring a pan of water to a gentle simmer, add vinegar.', 'Crack each egg into a small cup. Create a gentle whirlpool, slide egg in. Cook 3 minutes for runny yolk.', 'Spread avocado generously on toast. Top with poached egg.', 'Sprinkle with chilli flakes, everything bagel seasoning, and micro herbs. Serve at once.'],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with initial recipe data'

    def handle(self, *args, **options):
        Recipe.objects.all().delete()
        self.stdout.write('Cleared existing recipes.')

        for data in RECIPES:
            recipe = Recipe.objects.create(
                title=data['title'],
                category=data['category'],
                cuisine=data['cuisine'],
                time_minutes=data['time_minutes'],
                difficulty=data['difficulty'],
                calories=data['calories'],
                protein=data['protein'],
                carbs=data['carbs'],
                fat=data['fat'],
                image_url=data['image_url'],
                description=data['description'],
            )
            for idx, ing in enumerate(data['ingredients']):
                Ingredient.objects.create(recipe=recipe, name=ing, order=idx)
            for idx, step in enumerate(data['steps'], 1):
                CookingStep.objects.create(recipe=recipe, step_number=idx, instruction=step)
            self.stdout.write(f'  Created: {recipe.title}')

        self.stdout.write(self.style.SUCCESS(
            f'\nSeeding complete! '
            f'{Recipe.objects.count()} recipes, '
            f'{Ingredient.objects.count()} ingredients, '
            f'{CookingStep.objects.count()} steps in database.'
        ))
