# food/views.py
from rest_framework import viewsets, permissions
from .models import FoodEntry
from .serializers import FoodEntrySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

class FoodEntryViewSet(viewsets.ModelViewSet):
    serializer_class = FoodEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Return only food entries belonging to the current user and support simple filters
        qs = FoodEntry.objects.filter(user=self.request.user)
        date = self.request.query_params.get('date')
        meal_type = self.request.query_params.get('meal_type')
        if date:
            qs = qs.filter(date=date)
        if meal_type:
            qs = qs.filter(meal_type=meal_type)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='meal-summary')
    def meal_summary(self, request):
        """Return meal breakdown for a given date (query param `date` as YYYY-MM-DD)."""
        date = request.query_params.get('date')
        if not date:
            date = timezone.now().date().isoformat()
        summary = FoodEntry.meal_summary(request.user, date)
        return Response(summary, status=status.HTTP_200_OK)
