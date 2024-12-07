from rest_framework import serializers
from .models import FieldworkProject, FieldworkFile, Comment, Like, UserProfile
from django.conf import settings
import os
import uuid
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'display_name', 'user_type')
        read_only_fields = ('id', 'user_type')

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('username', 'display_name', 'password')
        
    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            display_name=validated_data['display_name'],
            password=validated_data['password']
        )
        return user

class FieldworkFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = FieldworkFile
        fields = '__all__'
        read_only_fields = ('file_path', 'uploaded_by', 'status', 'status_changed_at', 'status_changed_by')

    def get_file_url(self, obj):
        if obj.file_path:
            request = self.context.get('request')
            file_path = obj.file_path.replace('\\', '/')
            if request:
                return request.build_absolute_uri(f'/api/media/{file_path}')
            return f'/api/media/{file_path}'
        return None

    def create(self, validated_data):
        file_obj = validated_data.pop('file')
        file_extension = os.path.splitext(file_obj.name)[1].lower()
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}{file_extension}"
        
        file_type = validated_data.get('file_type', 'other')
        file_path = '/'.join(['uploads', file_type, unique_filename])
        absolute_path = os.path.join(settings.MEDIA_ROOT, *file_path.split('/'))
        
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
        
        with open(absolute_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        
        return FieldworkFile.objects.create(
            file_path=file_path,
            **validated_data
        )

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'project', 'file', 'created_at')

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('user', 'project', 'file', 'created_at')

class FieldworkProjectSerializer(serializers.ModelSerializer):
    investigator = UserSerializer(read_only=True)
    files = FieldworkFileSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.IntegerField(read_only=True)
    files_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = FieldworkProject
        fields = '__all__'

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return obj.likes.filter(id=user.id).exists() if user.is_authenticated else False

    def get_likes_count(self, obj):
        return obj.likes.count()