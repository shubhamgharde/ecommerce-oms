from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'contact', 'dob', 'address', 'aadhaar', 'marital_status', 'spouse_name')}),
        ('Work Info', {'fields': ('department', 'dpt_manager', 'qualification', 'designation', 'grade_pay', 'basic_pay', 'taxation', 'project')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'contact','dob', 'department', 'dpt_manager', 'qualification', 'designation', 'grade_pay', 'basic_pay', 'taxation', 'project'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
