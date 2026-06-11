# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardStatsView,
    RegisterView,
    LoginView,
    ProfileView,
    WeightEntryViewSet,
    GoalViewSet,
    MilestoneViewSet,
    DailyLogViewSet,
)

router = DefaultRouter()
router.register(r'weight-entries', WeightEntryViewSet, basename='weightentry')
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'milestones', MilestoneViewSet, basename='milestone')
router.register(r'daily-logs', DailyLogViewSet, basename='dailylog')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard'),
    path('', include(router.urls)),
]