from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserProfile, FieldworkProject, FieldworkFile, Comment, Like
from .serializers import (
    UserSerializer, 
    FieldworkProjectSerializer, 
    FieldworkFileSerializer,
    CommentSerializer,
    LikeSerializer
)
from django.http import FileResponse, Http404
from django.conf import settings
import os

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    只允许管理员修改，其他人只读
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class FieldworkProjectViewSet(viewsets.ModelViewSet):
    queryset = FieldworkProject.objects.all()
    serializer_class = FieldworkProjectSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # 获取或创建一个默认用户
        default_user, created = UserProfile.objects.get_or_create(
            username='default_user',
            defaults={
                'display_name': '默认用户',
                'is_active': True
            }
        )
        serializer.save(investigator=default_user)

    def get_queryset(self):
        view_type = self.request.query_params.get('view_type', 'all')
        queryset = self.queryset

        if view_type == 'public':
            # 资料广场：显示所有已审核通过的项目
            return queryset.filter(status='approved')
        elif view_type == 'my':
            # 我的项目：显示默认用户的项目
            return queryset.filter(investigator__username='default_user')
        else:
            # 所有项目
            return queryset

    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        """获取项目的所有文件"""
        project = self.get_object()
        # 如果项目已审核通过或者是项目创建者，则可以查看所有文件
        if project.status == 'approved' or (request.user.is_authenticated and project.investigator == request.user):
            files = project.files.all()
            serializer = FieldworkFileSerializer(files, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"detail": "项目未审核通过，暂时无法查看文件"}, status=status.HTTP_403_FORBIDDEN)

    def toggle_like(self, request, pk=None):
        project = self.get_object()
        # 获取或创建一个默认用户
        default_user, created = UserProfile.objects.get_or_create(
            username='default_user',
            defaults={
                'display_name': '默认用户',
                'is_active': True
            }
        )
        like, created = Like.objects.get_or_create(
            user=default_user,
            project=project
        )
        if not created:
            like.delete()
            return Response({'status': 'unliked'})
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        project = self.get_object()
        content = request.data.get('content')
        if not content:
            return Response(
                {'error': '评论内容不能为空'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        Comment.objects.create(
            user=request.user,
            project=project,
            content=content
        )
        return Response({'status': 'comment added'})

class FieldworkFileViewSet(viewsets.ModelViewSet):
    queryset = FieldworkFile.objects.all()
    serializer_class = FieldworkFileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """所有用户都能看到已审核通过的文件，管理员可以看到所有文件"""
        queryset = self.queryset
        project_id = self.request.query_params.get('project', None)
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        return queryset.filter(status='approved')

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """管理员审核通过文件"""
        if not request.user.is_staff:
            return Response({"detail": "只有管理员可以审核"}, status=status.HTTP_403_FORBIDDEN)
        
        file = self.get_object()
        file.status = 'approved'
        file.status_changed_at = timezone.now()
        file.status_changed_by = request.user
        file.save()
        return Response({"status": "approved"})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """管理员拒绝文件"""
        if not request.user.is_staff:
            return Response({"detail": "只有管理员可以审核"}, status=status.HTTP_403_FORBIDDEN)
        
        file = self.get_object()
        file.status = 'rejected'
        file.status_changed_at = timezone.now()
        file.status_changed_by = request.user
        file.save()
        return Response({"status": "rejected"})

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        """添加评论"""
        file = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, file=file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞或取消点赞"""
        file = self.get_object()
        like = Like.objects.filter(user=request.user, file=file).first()
        
        if like:
            like.delete()
            return Response({"detail": "取消点赞"})
        else:
            Like.objects.create(user=request.user, file=file)
            return Response({"detail": "点赞成功"})

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # 获取或创建一个默认用户
        default_user, created = UserProfile.objects.get_or_create(
            username='default_user',
            defaults={
                'display_name': '默认用户',
                'is_active': True
            }
        )
        
        # 确保文件在请求中
        if 'file' not in request.FILES:
            return Response({'error': '没有找到文件'}, status=status.HTTP_400_BAD_REQUEST)

        # 准备数据
        data = request.data.copy()
        data['file'] = request.FILES['file']
        
        file_serializer = FieldworkFileSerializer(data=data)
        if file_serializer.is_valid():
            file_serializer.save(uploaded_by=default_user)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def serve_media_file(request, file_path):
    # 构建完整的文件路径
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    print(f"Attempting to serve file: {full_path}")  # 调试输出
    
    # 检查文件是否存在
    if os.path.exists(full_path) and os.path.isfile(full_path):
        try:
            # 打开文件并返回
            file = open(full_path, 'rb')
            response = FileResponse(file)
            # 设置内容类型
            if file_path.endswith('.pdf'):
                response['Content-Type'] = 'application/pdf'
            elif file_path.endswith('.png'):
                response['Content-Type'] = 'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                response['Content-Type'] = 'image/jpeg'
            elif file_path.endswith('.mp3'):
                response['Content-Type'] = 'audio/mpeg'
            # 设置跨域头
            response['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            print(f"Error serving file: {e}")  # 调试输出
            raise Http404(f"Error serving file: {e}")
    else:
        print(f"File not found: {full_path}")  # 调试输出
        raise Http404("File not found")
