from django.contrib import admin
from .models import (
	WorkoutEntry,
	ScheduledWorkout,
	Exercise,
	WorkoutPlan,
	WorkoutPlanExercise,
	WorkoutGoal,
)


@admin.register(WorkoutEntry)
class WorkoutEntryAdmin(admin.ModelAdmin):
	list_display = ('user', 'exercise_name', 'duration_minutes', 'calories_burned', 'date', 'created_at')
	list_filter = ('date', 'user')
	search_fields = ('exercise_name', 'user__username')
	ordering = ('-date', '-created_at')


@admin.register(ScheduledWorkout)
class ScheduledWorkoutAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', 'scheduled_date', 'scheduled_time', 'completed')
	list_filter = ('scheduled_date', 'completed', 'user')
	search_fields = ('title', 'user__username')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
	list_display = ('name', 'muscle_group', 'default_sets', 'default_reps')
	search_fields = ('name', 'muscle_group')


class WorkoutPlanExerciseInline(admin.TabularInline):
	model = WorkoutPlanExercise
	extra = 0


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'difficulty', 'is_public', 'created_at')
	list_filter = ('difficulty', 'is_public')
	inlines = [WorkoutPlanExerciseInline]


@admin.register(WorkoutGoal)
class WorkoutGoalAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'status', 'target_value', 'current_value', 'created_at')
	list_filter = ('status',)
	search_fields = ('title', 'user__username')
