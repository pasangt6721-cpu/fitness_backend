# food/views.py
from rest_framework import viewsets, permissions
from .models import FoodEntry
from .serializers import FoodEntrySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta


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

    @action(detail=False, methods=['get'], url_path='weekly-summary')
    def weekly_summary(self, request):
        """Return daily calorie totals for the last 7 days ending on the given date."""
        date_str = request.query_params.get('date')
        try:
            end_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else timezone.now().date()
        except ValueError:
            end_date = timezone.now().date()

        days = []
        for i in range(6, -1, -1):
            day = end_date - timedelta(days=i)
            entries = FoodEntry.objects.filter(user=request.user, date=day)
            total_cal = sum(e.calories for e in entries)
            total_protein = sum(e.protein for e in entries)
            total_carbs = sum(e.carbs for e in entries)
            total_fat = sum(e.fat for e in entries)
            days.append({
                'date': day.isoformat(),
                'calories': total_cal,
                'protein': total_protein,
                'carbs': total_carbs,
                'fat': total_fat,
            })

        return Response(days, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='nutrition-streak')
    def nutrition_streak(self, request):
        """Return the consecutive-day streak of logging at least one food entry up to today."""
        today = timezone.now().date()
        streak = 0
        current = today

        while True:
            has_entry = FoodEntry.objects.filter(user=request.user, date=current).exists()
            if has_entry:
                streak += 1
                current -= timedelta(days=1)
            else:
                break

        return Response({'streak': streak, 'as_of': today.isoformat()}, status=status.HTTP_200_OK)
