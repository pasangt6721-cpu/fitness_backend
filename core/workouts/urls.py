# workouts/urls.py
from rest_framework.routers import DefaultRouter
from .views import (
	WorkoutEntryViewSet,
	ScheduledWorkoutViewSet,
	ExerciseViewSet,
	WorkoutPlanViewSet,
	WorkoutPlanExerciseViewSet,
	WorkoutGoalViewSet,
)

router = DefaultRouter()
router.register(r'workout-entries', WorkoutEntryViewSet, basename='workoutentry')
router.register(r'scheduled-workouts', ScheduledWorkoutViewSet, basename='scheduledworkout')
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'workout-plans', WorkoutPlanViewSet, basename='workoutplan')
router.register(r'plan-exercises', WorkoutPlanExerciseViewSet, basename='planexercise')
router.register(r'workout-goals', WorkoutGoalViewSet, basename='workoutgoal')

urlpatterns = router.urls