# workouts/models.py
from django.db import models
from django.conf import settings

class WorkoutEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_entries')
    exercise_name = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    calories_burned = models.PositiveIntegerField(help_text="Estimated calories burned")
    date = models.DateField(help_text="Date of workout")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise_name} on {self.date}"