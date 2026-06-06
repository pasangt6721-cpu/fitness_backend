# food/views.py
from rest_framework import viewsets, permissions
from .models import FoodEntry
from .serializers import FoodEntrySerializer

class FoodEntryViewSet(viewsets.ModelViewSet):
    serializer_class = FoodEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Return only food entries belonging to the current user
        return FoodEntry.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
