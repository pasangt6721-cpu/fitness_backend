from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	fieldsets = BaseUserAdmin.fieldsets + (
		('Additional info', {'fields': ('bio', 'profile_picture')}),
	)
	list_display = ('username', 'email', 'is_staff', 'is_superuser')
	search_fields = ('username', 'email')
