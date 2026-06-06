# workouts/serializers.py
from rest_framework import serializers
from .models import WorkoutEntry

class WorkoutEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutEntry
        fields = ['id', 'user', 'exercise_name', 'duration_minutes', 'calories_burned', 'date', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']