# food/models.py
from django.db import models
from django.conf import settings

class FoodEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='food_entries')
    food_name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField(help_text="Calories consumed")
    protein = models.PositiveIntegerField(default=0, help_text="Protein in grams")
    carbs = models.PositiveIntegerField(default=0, help_text="Carbohydrates in grams")
    fat = models.PositiveIntegerField(default=0, help_text="Fat in grams")
    date = models.DateField(auto_now_add=False, help_text="Date when food was eaten")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']   # newest first
    
    def __str__(self):
        return f"{self.user.username} - {self.food_name} on {self.date}"