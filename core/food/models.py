# food/models.py (or accounts/models.py)

from django.db import models
from django.conf import settings
from django.utils import timezone

class FoodEntry(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='food_entries')
    food_name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField(help_text="Calories consumed")
    protein = models.PositiveIntegerField(default=0, help_text="Protein in grams")
    carbs = models.PositiveIntegerField(default=0, help_text="Carbohydrates in grams")
    fat = models.PositiveIntegerField(default=0, help_text="Fat in grams")
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES,
        default='lunch',
        help_text="Which meal this food belongs to (breakfast, lunch, snacks, dinner)"
    )
    date = models.DateField(
        default=timezone.now,
        help_text="Date when food was eaten"
    )
    time = models.TimeField(
        blank=True, null=True,
        help_text="Optional: exact time of meal (e.g., 08:00 for breakfast)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'meal_type']),   # for filtering by meal type
        ]

    def __str__(self):
        return f"{self.user.username} - {self.food_name} ({self.get_meal_type_display()}) on {self.date}"

    @classmethod
    def daily_summary(cls, user, date):
        """Return total calories, protein, carbs, fat for a given user and date."""
        entries = cls.objects.filter(user=user, date=date)
        if not entries:
            return None
        totals = {
            'calories': sum(e.calories for e in entries),
            'protein': sum(e.protein for e in entries),
            'carbs': sum(e.carbs for e in entries),
            'fat': sum(e.fat for e in entries),
        }
        return totals

    @classmethod
    def meal_summary(cls, user, date):
        """Return a breakdown by meal type for a given date.
        Example output:
        {
            'breakfast': {'calories': 350, 'protein': 15, ...},
            'lunch': {...},
            'snacks': {...},
            'dinner': {...}
        }
        """
        entries = cls.objects.filter(user=user, date=date)
        result = {meal_type: {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
                  for meal_type, _ in cls.MEAL_TYPE_CHOICES}
        for entry in entries:
            meal = entry.meal_type
            result[meal]['calories'] += entry.calories
            result[meal]['protein'] += entry.protein
            result[meal]['carbs'] += entry.carbs
            result[meal]['fat'] += entry.fat
        return result