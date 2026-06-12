# workouts/serializers.py
from rest_framework import serializers
from .models import (
    WorkoutEntry,
    ScheduledWorkout,
    Exercise,
    WorkoutPlan,
    WorkoutPlanExercise,
    WorkoutGoal,
)


class WorkoutEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutEntry
        fields = ['id', 'user', 'exercise_name', 'duration_minutes', 'calories_burned', 'date', 'time', 'notes', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ScheduledWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledWorkout
        fields = ['id', 'user', 'title', 'description', 'difficulty', 'scheduled_date', 'scheduled_time', 'duration_minutes', 'exercises_count', 'completed', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'default_sets', 'default_reps', 'default_duration_seconds', 'muscle_group']
        read_only_fields = ['id']


class WorkoutPlanExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutPlanExercise
        fields = ['id', 'workout_plan', 'exercise', 'sets', 'reps', 'duration_seconds', 'order']
        read_only_fields = ['id']


class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = WorkoutPlanExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'user', 'title', 'description', 'difficulty', 'is_public', 'created_at', 'exercises']
        read_only_fields = ['id', 'user', 'created_at']


class WorkoutGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()

    class Meta:
        model = WorkoutGoal
        fields = ['id', 'user', 'title', 'description', 'target_value', 'current_value', 'unit', 'period_days', 'status', 'target_date', 'achieved_date', 'created_at', 'progress_percentage']
        read_only_fields = ['id', 'user', 'created_at', 'progress_percentage']