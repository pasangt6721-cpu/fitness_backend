from django.contrib import admin
from .models import WorkoutEntry


@admin.register(WorkoutEntry)
class WorkoutEntryAdmin(admin.ModelAdmin):
	list_display = ('user', 'exercise_name', 'duration_minutes', 'calories_burned', 'date', 'created_at')
	list_filter = ('date', 'user')
	search_fields = ('exercise_name', 'user__username')
	ordering = ('-date', '-created_at')
