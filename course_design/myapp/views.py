from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import FileResponse, Http404
from django.conf import settings
import os
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny

from .models import Survey, MediaItem, UserProfile
from .serializers import SurveySerializer, MediaItemSerializer, UserProfileSerializer

class SurveyViewSet(viewsets.ModelViewSet):
    """调查记录的视图集"""
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    permission_classes = [permissions.AllowAny]  # 允许所有人访问
    
    def get_queryset(self):
        """获取查询集，支持过滤"""
        queryset = Survey.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """创建时自动设置调查人"""
        if self.request.user.is_authenticated:
            serializer.save(investigator=self.request.user)
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def upload_media(self, request, pk=None):
        """上传媒体文件到特定调查"""
        survey = self.get_object()
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': '没有文件被上传'}, status=status.HTTP_400_BAD_REQUEST)
        
        media_data = {
            'survey': survey.id,
            'title': request.data.get('title', ''),
            'description': request.data.get('description', ''),
            'media_type': request.data.get('media_type'),
            'category': request.data.get('category'),
            'file_path': file_obj
        }
        
        serializer = MediaItemSerializer(data=media_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        print("接收到的数据:", request.data)  # 调试日志
        return super().create(request, *args, **kwargs)

class MediaItemViewSet(viewsets.ModelViewSet):
    """媒体资料的视图集"""
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        queryset = MediaItem.objects.all()
        survey_id = self.request.query_params.get('survey', None)
        if survey_id is not None:
            queryset = queryset.filter(survey_id=survey_id)
        return queryset

def serve_media_file(request, file_path):
    """服务媒体文件的视图函数"""
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    if os.path.exists(full_path) and os.path.isfile(full_path):
        try:
            file = open(full_path, 'rb')
            response = FileResponse(file)
            
            # 设置合适的Content-Type
            if file_path.endswith('.pdf'):
                response['Content-Type'] = 'application/pdf'
            elif file_path.endswith('.png'):
                response['Content-Type'] = 'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                response['Content-Type'] = 'image/jpeg'
            elif file_path.endswith('.mp3'):
                response['Content-Type'] = 'audio/mpeg'
            elif file_path.endswith('.mp4'):
                response['Content-Type'] = 'video/mp4'
                
            return response
        except Exception as e:
            raise Http404(f"Error serving file: {e}")
    else:
        raise Http404("File not found")

class UserProfileViewSet(viewsets.ModelViewSet):
    """用户配置的视图集"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': '请提供用户名和密码'}, status=400)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({'error': '用户名或密码错误'}, status=401)
    
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'display_name': getattr(user, 'display_name', user.username),
            'user_type': getattr(user, 'user_type', 'user')
        }
    })

@api_view(['POST'])
def logout(request):
    if request.user.is_authenticated:
        Token.objects.filter(user=request.user).delete()
    return Response({'message': '已登出'})
