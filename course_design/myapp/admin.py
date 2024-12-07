from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, FieldworkProject, FieldworkFile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'display_name', 'user_type', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'display_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('display_name', 'user_type')}),
        ('权限', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'display_name', 'password1', 'password2'),
        }),
    )

# 注册模型
admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(FieldworkProject)
admin.site.register(FieldworkFile)
