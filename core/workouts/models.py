# workout/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class WorkoutEntry(models.Model):
    """A completed workout – used for history, totals, streak, and calories."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_entries')
    exercise_name = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    calories_burned = models.PositiveIntegerField(help_text="Estimated calories burned")
    date = models.DateField(default=timezone.now, help_text="Date of workout")
    time = models.TimeField(blank=True, null=True, help_text="Optional: time of workout")
    notes = models.TextField(blank=True, help_text="Sets, reps, intensity, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} – {self.exercise_name} on {self.date}"
    
    @property
    def duration_hours(self):
        return self.duration_minutes / 60.0
    
    @classmethod
    def monthly_summary(cls, user, year=None, month=None):
        """Return {'workouts': n, 'calories': n, 'hours': n} for given month (default current)."""
        if year is None:
            year = timezone.now().year
        if month is None:
            month = timezone.now().month
        qs = cls.objects.filter(user=user, date__year=year, date__month=month)
        if not qs:
            return {'workouts': 0, 'calories': 0, 'hours': 0.0}
        return {
            'workouts': qs.count(),
            'calories': sum(e.calories_burned for e in qs),
            'hours': round(sum(e.duration_minutes for e in qs) / 60.0, 1),
        }
    
    @classmethod
    def current_streak(cls, user):
        """Consecutive days with at least one workout, ending today."""
        workout_dates = cls.objects.filter(user=user).dates('date', 'day').order_by('-date')
        if not workout_dates:
            return 0
        streak = 0
        expected = timezone.now().date()
        for d in workout_dates:
            if d == expected:
                streak += 1
                expected -= timezone.timedelta(days=1)
            else:
                break
        return streak


class ScheduledWorkout(models.Model):
    """Upcoming planned workout (appears in 'Upcoming Workouts' list)."""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scheduled_workouts')
    title = models.CharField(max_length=200)          # e.g. "Full Body Strength"
    description = models.TextField(blank=True)        # e.g. "8 exercises"
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    exercises_count = models.PositiveSmallIntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['scheduled_date', 'scheduled_time']
        indexes = [
            models.Index(fields=['user', 'scheduled_date', 'completed']),
        ]
    
    def __str__(self):
        return f"{self.user.username} – {self.title} on {self.scheduled_date}"


class Exercise(models.Model):
    """A single exercise (e.g. Push‑ups, Squats) used in Quick Start and Workout Plans."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    default_sets = models.PositiveSmallIntegerField(default=3)
    default_reps = models.PositiveSmallIntegerField(default=10)
    default_duration_seconds = models.PositiveSmallIntegerField(blank=True, null=True, help_text="For timed exercises like Plank")
    muscle_group = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    """A structured workout routine (e.g. 'Full Body Strength' with multiple exercises)."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_plans', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=ScheduledWorkout.DIFFICULTY_CHOICES, default='intermediate')
    is_public = models.BooleanField(default=False)   # allow sharing between users
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class WorkoutPlanExercise(models.Model):
    """Junction table: which exercises belong to a WorkoutPlan, with custom sets/reps."""
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveSmallIntegerField(default=3)
    reps = models.PositiveSmallIntegerField(default=10)
    duration_seconds = models.PositiveSmallIntegerField(blank=True, null=True)  # override for timed exercises
    order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        unique_together = ['workout_plan', 'exercise']
    
    def __str__(self):
        return f"{self.workout_plan.title} – {self.exercise.name}"


class WorkoutGoal(models.Model):
    """User's workout‑related goals (e.g. '4 workouts per week', 'Run 5 km', '100 push‑ups')."""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('achieved', 'Achieved'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_goals')
    title = models.CharField(max_length=100)          # e.g. "4 workouts per week"
    description = models.TextField(blank=True)        # e.g. "Complete 4 workout sessions every week"
    target_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Target number (e.g. 4 workouts)")
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=20, default='workouts', help_text="e.g. workouts, km, push-ups")
    period_days = models.PositiveSmallIntegerField(default=7, help_text="Goal period in days (e.g. weekly goal = 7)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    target_date = models.DateField(blank=True, null=True)
    achieved_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} – {self.title} ({self.status})"
    
    @property
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        percent = (self.current_value / self.target_value) * 100
        return min(100, int(percent))