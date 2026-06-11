# accounts/serializers.py
from rest_framework import serializers
from .models import User, WeightEntry, Goal, Milestone, DailyLog


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'current_weight_kg']
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    """Basic user info – good for profiles."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'current_weight_kg']
        read_only_fields = ['id']


class WeightEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightEntry
        fields = ['id', 'user', 'weight_kg', 'date', 'note']
        read_only_fields = ['id']


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'title', 'description', 'target_value', 'target_unit',
                  'current_value', 'target_date', 'status', 'achieved_date', 'created_at']
        read_only_fields = ['id', 'created_at']


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ['id', 'user', 'goal', 'title', 'achieved', 'achieved_date']
        read_only_fields = ['id']


class DailyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLog
        fields = ['id', 'user', 'date', 'workouts_count', 'water_liters', 'calories']
        read_only_fields = ['id']