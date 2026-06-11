# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Extended user with basic health profile."""
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    # Simple weight field (not auto‑synced – intern can update manually)
    current_weight_kg = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return self.username


class WeightEntry(models.Model):
    """Record weight on a specific date. Helps track progress over time."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_entries')
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1)
    date = models.DateField(default=timezone.now)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} – {self.weight_kg}kg on {self.date}"


class Goal(models.Model):
    """A personal goal, e.g., 'Reach 55 kg', 'Workout 5 times a week'."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=100)          # e.g. "Reach 55 kg"
    description = models.TextField(blank=True)        # e.g. "62.5 kg → 55 kg"
    target_value = models.DecimalField(max_digits=10, decimal_places=2)   # e.g. 55 (kg) or 5 (times/week)
    target_unit = models.CharField(max_length=20, blank=True, default='kg') # kg, times/week, liters, kcal
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_date = models.DateField(null=True, blank=True)
    # Status: 'in_progress' or 'achieved'
    status = models.CharField(max_length=20, default='in_progress')
    achieved_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – {self.title}"


class Milestone(models.Model):
    """A small achievement like 'Lost 5 kg' or 'Workout 10 times'."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='milestones')
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True, related_name='milestones')
    title = models.CharField(max_length=100)          # e.g. "Lost 5 kg"
    achieved = models.BooleanField(default=False)
    achieved_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} – {'Achieved' if self.achieved else 'In progress'}"


class DailyLog(models.Model):
    """What the user did on a single day – used to update goal progress."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField(default=timezone.now)
    workouts_count = models.PositiveSmallIntegerField(default=0)   # number of workouts done today
    water_liters = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    calories = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['user', 'date']   # only one log per user per day
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} – {self.date}"