# workouts/views.py
from rest_framework import viewsets, permissions
from .models import WorkoutEntry
from .serializers import WorkoutEntrySerializer

class WorkoutEntryViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return WorkoutEntry.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)