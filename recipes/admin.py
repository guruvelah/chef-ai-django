from django.contrib import admin
from .models import Recipe, Ingredient, CookingStep, ChatLog, Bookmark


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class CookingStepInline(admin.TabularInline):
    model = CookingStep
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'cuisine', 'time_minutes', 'difficulty', 'calories', 'created_at']
    list_filter = ['category', 'cuisine', 'difficulty']
    search_fields = ['title', 'description']
    inlines = [IngredientInline, CookingStepInline]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'image_url')
        }),
        ('Classification', {
            'fields': ('category', 'cuisine', 'difficulty', 'time_minutes')
        }),
        ('Nutrition', {
            'fields': ('calories', 'protein', 'carbs', 'fat')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'recipe', 'order']
    list_filter = ['recipe__category']
    search_fields = ['name', 'recipe__title']


@admin.register(CookingStep)
class CookingStepAdmin(admin.ModelAdmin):
    list_display = ['step_number', 'recipe', 'instruction']
    list_filter = ['recipe__cuisine']
    search_fields = ['instruction', 'recipe__title']


@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user_message', 'response_type', 'session_key']
    list_filter = ['response_type', 'timestamp']
    search_fields = ['user_message', 'ai_reply']
    readonly_fields = ['timestamp', 'session_key', 'user_message', 'ai_reply', 'response_type']

    def has_add_permission(self, request):
        return False


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'session_key', 'saved_at']
    list_filter = ['saved_at']
    readonly_fields = ['saved_at']
