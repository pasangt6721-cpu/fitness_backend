# workouts/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    WorkoutEntry,
    ScheduledWorkout,
    Exercise,
    WorkoutPlan,
    WorkoutPlanExercise,
    WorkoutGoal,
)
from .serializers import (
    WorkoutEntrySerializer,
    ScheduledWorkoutSerializer,
    ExerciseSerializer,
    WorkoutPlanSerializer,
    WorkoutPlanExerciseSerializer,
    WorkoutGoalSerializer,
)


class _UserScopedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutEntryViewSet(_UserScopedModelViewSet):
    model = WorkoutEntry
    queryset = WorkoutEntry.objects.all()
    serializer_class = WorkoutEntrySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        entry_date = self.request.query_params.get('date')
        if entry_date:
            qs = qs.filter(date=entry_date)
        return qs

    @action(detail=False, methods=['get'])
    def streak(self, request):
        streak_val = WorkoutEntry.current_streak(request.user)
        return Response({'streak': streak_val})


class ScheduledWorkoutViewSet(_UserScopedModelViewSet):
    model = ScheduledWorkout
    queryset = ScheduledWorkout.objects.all()
    serializer_class = ScheduledWorkoutSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        selected_date = self.request.query_params.get('date')
        if selected_date:
            qs = qs.filter(scheduled_date__gte=selected_date)
        return qs


class ExerciseViewSet(viewsets.ModelViewSet):
    """Exercises are global objects; allow read/write for authenticated users."""
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # allow public plans for anyone; limit personal plans to owner
        qs = WorkoutPlan.objects.filter(is_public=True)
        if self.request.user.is_authenticated:
            qs = qs | WorkoutPlan.objects.filter(user=self.request.user)
        return qs.distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutPlanExerciseViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlanExercise.objects.all()
    serializer_class = WorkoutPlanExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow managing exercises for plans the user owns
        return WorkoutPlanExercise.objects.filter(workout_plan__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class WorkoutGoalViewSet(_UserScopedModelViewSet):
    model = WorkoutGoal
    queryset = WorkoutGoal.objects.all()
    serializer_class = WorkoutGoalSerializer