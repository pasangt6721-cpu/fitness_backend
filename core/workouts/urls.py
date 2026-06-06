# workouts/urls.py
from rest_framework.routers import DefaultRouter
from .views import WorkoutEntryViewSet

router = DefaultRouter()
router.register(r'workout-entries', WorkoutEntryViewSet, basename='workoutentry')

urlpatterns = router.urls