from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, display_name, password=None, **extra_fields):
        if not username:
            raise ValueError('用户名必须提供')
        user = self.model(
            username=username,
            display_name=display_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, display_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        return self.create_user(username, display_name, password, **extra_fields)

class UserProfile(AbstractUser):
    """用户模型"""
    phone = models.CharField(max_length=11, blank=True, verbose_name='手机号')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

class Survey(models.Model):
    """调查记录模型"""
    name = models.CharField(max_length=100, verbose_name='调查名称')
    longitude = models.FloatField(verbose_name='经度')
    latitude = models.FloatField(verbose_name='纬度')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    investigator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='调查人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

class MediaItem(models.Model):
    """媒体资料模型"""
    MEDIA_TYPES = (
        ('IMAGE', '图片'),
        ('AUDIO', '音频'),
        ('VIDEO', '视频'),
        ('DOCUMENT', '文档'),
    )
    
    CATEGORY_TYPES = (
        ('FOLKLORE', '风土人情'),
        ('INTERVIEW', '访谈记录'),
        ('LITERATURE', '文献资料'),
    )

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='media_items', verbose_name='所属调查')
    title = models.CharField(max_length=200, verbose_name='标题')
    description = models.TextField(blank=True, verbose_name='描述')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, verbose_name='媒体类型')
    category = models.CharField(max_length=10, choices=CATEGORY_TYPES, verbose_name='资料分类')
    file_path = models.FileField(upload_to='survey_files/%Y/%m/', verbose_name='文件路径')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    def __str__(self):
        return self.title
