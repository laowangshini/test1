from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Survey, MediaItem

class MediaItemInline(admin.TabularInline):
    model = MediaItem
    extra = 1

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'investigator', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'investigator__username')
    inlines = [MediaItemInline]

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'survey', 'media_type', 'category', 'created_at')
    list_filter = ('media_type', 'category')
    search_fields = ('title', 'description', 'survey__name')

# 使用Django默认的UserAdmin，但注册我们的UserProfile模型
admin.site.register(UserProfile, UserAdmin)
