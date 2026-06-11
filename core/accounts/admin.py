from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, WeightEntry, Goal, Milestone, DailyLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	fieldsets = BaseUserAdmin.fieldsets + (
		('Additional info', {'fields': ('bio', 'profile_picture', 'current_weight_kg')}),
	)
	list_display = ('username', 'email', 'current_weight_kg', 'is_staff', 'is_superuser')
	search_fields = ('username', 'email')


@admin.register(WeightEntry)
class WeightEntryAdmin(admin.ModelAdmin):
	list_display = ('user', 'weight_kg', 'date')
	search_fields = ('user__username',)
	date_hierarchy = 'date'
	list_filter = ('date',)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'target_value', 'target_unit', 'status', 'target_date')
	search_fields = ('title', 'user__username')
	list_filter = ('status', 'target_unit')
	date_hierarchy = 'created_at'


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'goal', 'achieved', 'achieved_date')
	search_fields = ('title', 'user__username', 'goal__title')
	list_filter = ('achieved',)


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
	list_display = ('user', 'date', 'workouts_count', 'water_liters', 'calories')
	search_fields = ('user__username',)
	date_hierarchy = 'date'
	list_filter = ('date',)
