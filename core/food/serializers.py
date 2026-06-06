# food/serializers.py
from rest_framework import serializers
from .models import FoodEntry

class FoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodEntry
        fields = ['id', 'user', 'food_name', 'calories', 'protein', 'carbs', 'fat', 'date', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        # Automatically set the user to the logged-in user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)