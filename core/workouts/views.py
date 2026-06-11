# workouts/views.py
from rest_framework import viewsets, permissions
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


class ScheduledWorkoutViewSet(_UserScopedModelViewSet):
    model = ScheduledWorkout
    queryset = ScheduledWorkout.objects.all()
    serializer_class = ScheduledWorkoutSerializer


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