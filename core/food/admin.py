from django.contrib import admin
from .models import FoodEntry


@admin.register(FoodEntry)
class FoodEntryAdmin(admin.ModelAdmin):
	list_display = ('user', 'food_name', 'meal_type', 'calories', 'date', 'created_at')
	list_filter = ('date', 'user', 'meal_type')
	search_fields = ('food_name', 'user__username')
	ordering = ('-date', '-created_at')
