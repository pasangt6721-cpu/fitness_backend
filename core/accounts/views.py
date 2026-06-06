# accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserSerializer, ProfileUpdateSerializer
from .models import User
from django.utils import timezone
from datetime import date

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]   # anyone can register
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Generate tokens for immediate login
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user   # returns the logged-in user

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        today = date.today()
        user = request.user
        
        # Food entries today
        food_today = user.food_entries.filter(date=today)
        total_calories_consumed = sum(f.calories for f in food_today)
        total_protein = sum(f.protein for f in food_today)
        total_carbs = sum(f.carbs for f in food_today)
        total_fat = sum(f.fat for f in food_today)
        
        # Workout entries today
        workout_today = user.workout_entries.filter(date=today)
        total_calories_burned = sum(w.calories_burned for w in workout_today)
        total_duration = sum(w.duration_minutes for w in workout_today)
        
        # Optionally, last 7 days food/calories summary (for charts)
        last_7_days = [today - timezone.timedelta(days=i) for i in range(7)]
        weekly_food_calories = []
        for d in last_7_days:
            total = sum(f.calories for f in user.food_entries.filter(date=d))
            weekly_food_calories.append({'date': d.isoformat(), 'calories': total})
        
        data = {
            'today': {
                'calories_consumed': total_calories_consumed,
                'calories_burned': total_calories_burned,
                'net_calories': total_calories_consumed - total_calories_burned,
                'protein_g': total_protein,
                'carbs_g': total_carbs,
                'fat_g': total_fat,
                'workout_minutes': total_duration,
            },
            'weekly_food_calories': weekly_food_calories,
        }
        return Response(data)