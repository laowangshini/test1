from django.contrib.auth import authenticate, login as auth_login
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer, UserRegisterSerializer
import logging
import traceback
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'display_name', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户ID (4-20位字母或数字)'),
            'display_name': openapi.Schema(type=openapi.TYPE_STRING, description='显示名称'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码 (8-20位，必须包含字母和数字)'),
        }
    ),
    responses={
        201: openapi.Response(
            description='注册成功',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                }
            )
        ),
        400: openapi.Response(description='请求数据无效'),
        500: openapi.Response(description='服务器错误'),
    }
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    用户注册 API
    
    注册新用户，需要提供：
    * username: 用户ID (4-20位字母或数字)
    * display_name: 显示名称
    * password: 密码 (8-20位，必须包含字母和数字)
    """
    try:
        # 记录请求数据（去除密码信息）
        safe_data = request.data.copy()
        if 'password' in safe_data:
            safe_data['password'] = '******'
        logger.info(f"收到注册请求: {safe_data}")
        
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            auth_login(request, user)
            
            response_data = {
                'message': '注册成功',
                'user': UserSerializer(user).data
            }
            logger.info(f"用户注册成功: {user.username}")
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"注册数据验证失败: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"注册过程中发生错误: {str(e)}")
        logger.error(f"错误详情: {traceback.format_exc()}")
        return Response({
            'error': '注册失败，请稍后重试'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户ID'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
        }
    ),
    responses={
        200: openapi.Response(
            description='登录成功',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                }
            )
        ),
        401: openapi.Response(description='认证失败'),
        500: openapi.Response(description='服务器错误'),
    }
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    用户登录 API
    
    使用用户ID和密码登录系统
    """
    try:
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        
        logger.info(f"尝试登录用户: {username}")
        
        # 验证用户
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # 登录用户，这会创建会话
            auth_login(request, user)
            
            # 设置会话过期时间（7天）
            request.session.set_expiry(60 * 60 * 24 * 7)
            
            # 准备响应数据
            response_data = {
                'message': '登录成功',
                'user': UserSerializer(user).data
            }
            logger.info(f"用户登录成功: {username}, 响应数据: {response_data}")
            return Response(response_data)
        else:
            logger.warning(f"用户登录失败，用户名或密码错误: {username}")
            return Response({
                'error': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except Exception as e:
        logger.error(f"登录错误: {str(e)}")
        logger.error(f"错误详情: {traceback.format_exc()}")
        return Response({
            'error': '登录失败，请稍后重试'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description='获取用户信息成功',
            schema=UserSerializer
        ),
        401: openapi.Response(description='未登录'),
    }
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_info(request):
    """
    获取当前用户信息 API
    
    返回当前登录用户的详细信息
    """
    try:
        if not request.user.is_authenticated:
            return Response({
                'error': '未登录'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # 更新会话过期时间
        request.session.set_expiry(60 * 60 * 24 * 7)  # 7天
        
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"获取用户信息错误: {str(e)}")
        return Response({
            'error': '获取用户信息失败'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def logout(request):
    """
    用户登出 API
    
    清除用户的会话信息
    """
    try:
        # 清除会话
        request.session.flush()
        return Response({'message': '登出成功'})
    except Exception as e:
        logger.error(f"登出错误: {str(e)}")
        return Response({
            'error': '登出失败，请稍后重试'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 