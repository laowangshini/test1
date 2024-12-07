from django.urls import path, re_path
from . import views
from . import auth

urlpatterns = [
    # 认证相关
    path('auth/register/', auth.register, name='register'),
    path('auth/login/', auth.login, name='login'),
    path('auth/logout/', auth.logout, name='logout'),
    path('auth/user-info/', auth.user_info, name='user_info'),
    
    # 项目相关
    path('projects/', views.FieldworkProjectViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='project-list'),
    path('projects/<int:pk>/', views.FieldworkProjectViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='project-detail'),
    path('projects/<int:pk>/like/', views.FieldworkProjectViewSet.as_view({
        'post': 'toggle_like'
    }), name='project-like'),
    path('projects/<int:pk>/files/', views.FieldworkProjectViewSet.as_view({
        'get': 'files'
    }), name='project-files'),
    
    # 文件相关
    path('files/upload/', views.FileUploadView.as_view(), name='file-upload'),
    path('files/<int:pk>/', views.FieldworkFileViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    }), name='file-detail'),
    
    # 媒体文件服务
    re_path(r'^media/(?P<file_path>.*)$', views.serve_media_file, name='serve-media'),
] 