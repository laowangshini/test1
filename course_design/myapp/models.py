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
    """自定义用户模型"""
    USER_TYPES = (
        ('user', '普通用户'),
        ('admin', '管理员'),
    )
    
    username = models.CharField('用户ID', max_length=20, unique=True)
    display_name = models.CharField('显示名称', max_length=50)
    user_type = models.CharField('用户类型', max_length=20, choices=USER_TYPES, default='user')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return f'{self.username} ({self.display_name})'

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        swappable = 'AUTH_USER_MODEL'

class FieldworkProject(models.Model):
    """田野调查项目"""
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )
    
    title = models.CharField('主题名称', max_length=100)
    latitude = models.FloatField('纬度')
    longitude = models.FloatField('经度')
    start_date = models.DateField('开始日期')
    end_date = models.DateField('结束日期')
    investigator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='调查人')
    status = models.CharField('审核状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    status_changed_at = models.DateTimeField('状态更新时间', null=True, blank=True)
    status_changed_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, 
                                        related_name='reviewed_projects', verbose_name='审核人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '田野调查项目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

class FieldworkFile(models.Model):
    """调查资料文件"""
    FILE_TYPES = (
        ('image', '图片'),
        ('audio', '音频'),
        ('video', '视频'),
        ('document', '文献'),
    )
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )

    project = models.ForeignKey(FieldworkProject, on_delete=models.CASCADE, related_name='files', verbose_name='所属项目')
    file_type = models.CharField('文件类型', max_length=20, choices=FILE_TYPES)
    title = models.CharField('文件标题', max_length=200)
    description = models.TextField('描述', blank=True)
    file_path = models.CharField('文件路径', max_length=500)
    uploaded_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='上传者')
    status = models.CharField('审核状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    status_changed_at = models.DateTimeField('状态更新时间', null=True, blank=True)
    status_changed_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='reviewed_files', verbose_name='审核人')
    uploaded_at = models.DateTimeField('上传时间', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '调查资料文件'
        verbose_name_plural = verbose_name
        ordering = ['-uploaded_at']

class Comment(models.Model):
    """评论"""
    project = models.ForeignKey(FieldworkProject, on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='comments', verbose_name='项目')
    file = models.ForeignKey(FieldworkFile, on_delete=models.CASCADE, null=True, blank=True,
                           related_name='comments', verbose_name='文件')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.TextField('评论内容')
    created_at = models.DateTimeField('评论时间', auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}的评论'

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

class Like(models.Model):
    """点赞"""
    project = models.ForeignKey(FieldworkProject, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='likes', verbose_name='项目')
    file = models.ForeignKey(FieldworkFile, on_delete=models.CASCADE, null=True, blank=True,
                           related_name='likes', verbose_name='文件')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='点赞者')
    created_at = models.DateTimeField('点赞时间', auto_now_add=True)

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name
        unique_together = [['user', 'project'], ['user', 'file']]  # 同一用户不能重复点赞
