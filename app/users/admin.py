from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'date_joined')

    search_fields = ('username', 'email', 'first_name', 'last_name')

    list_filter = ('is_staff', 'date_joined')

    list_editable = ('is_staff',)

    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups',
            'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'password1',
                'password2', 'is_staff'),
        }),
    )

    def get_queryset(self, request):
        # Фильтруем только активных пользователей
        return User.objects.filter(is_active=True)


admin.site.register(User, CustomUserAdmin)
