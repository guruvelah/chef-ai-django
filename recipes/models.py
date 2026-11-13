from django.db import models


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('High Protein', 'High Protein'),
        ('Quick', 'Quick (<20 min)'),
        ('Vegetarian', 'Vegetarian'),
        ('Low Carb', 'Low Carb'),
        ('Dessert', 'Dessert'),
    ]
    CUISINE_CHOICES = [
        ('Italian', 'Italian'),
        ('Asian', 'Asian'),
        ('Indian', 'Indian'),
        ('Mediterranean', 'Mediterranean'),
        ('American', 'American'),
        ('French', 'French'),
    ]
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    cuisine = models.CharField(max_length=50, choices=CUISINE_CHOICES)
    time_minutes = models.PositiveIntegerField(help_text='Cooking time in minutes')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Medium')
    calories = models.PositiveIntegerField()
    protein = models.CharField(max_length=20)
    carbs = models.CharField(max_length=20)
    fat = models.CharField(max_length=20)
    image_url = models.URLField(max_length=500)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.cuisine})"


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} → {self.recipe.title}"


class CookingStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    step_number = models.PositiveSmallIntegerField()
    instruction = models.TextField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.recipe.title}"


class ChatLog(models.Model):
    session_key = models.CharField(max_length=100, blank=True)
    user_message = models.TextField()
    ai_reply = models.TextField()
    response_type = models.CharField(max_length=50, default='general')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp:%d %b %Y %H:%M}] {self.user_message[:60]}"


class Bookmark(models.Model):
    session_key = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['session_key', 'recipe']
        ordering = ['-saved_at']

    def __str__(self):
        return f"Bookmark: {self.recipe.title}"
