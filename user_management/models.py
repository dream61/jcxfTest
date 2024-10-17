from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# 自定义用户管理器
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('用户必须有一个邮箱地址')
        if not username:
            raise ValueError('用户必须有一个用户名')

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# 用户模型
class Users(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    status = models.BooleanField(default=True)  # 用户状态（是否激活）
    is_logged_in = models.BooleanField(default=False)  # 是否登录
    project = models.CharField(max_length=255, blank=True, null=True)  # 所属项目
    module = models.CharField(max_length=255, blank=True, null=True)  # 所属模块
    # 权限相关字段
    is_staff = models.BooleanField(default=False)  # 是否是员工
    is_superuser = models.BooleanField(default=False)  # 是否是超级用户


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()  # 关联自定义用户管理器

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息表'
        verbose_name_plural = '用户信息表'

