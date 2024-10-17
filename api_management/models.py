from django.db import models
from project_management.models import Project
from module_management.models import Module
from user_management.models import Users

# Create your models here.
class ApiInterface(models.Model):
    
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    
    REQUEST_METHOD_CHOICES = [
        (GET, 'GET'),
        (POST, 'POST'),
        (PUT, 'PUT'),
        (DELETE, 'DELETE'),
        (PATCH, 'PATCH'),
        (HEAD, 'HEAD'),
        (OPTIONS, 'OPTIONS')
    ]

    STATUS_CHOICES = [
        ('active', '启用'),
        ('inactive', '停用'),
        ('maintenance', '维护中')
    ]

    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="所属项目")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name="所属模块")
    name = models.CharField(max_length=200, verbose_name="接口名称")
    url = models.CharField(max_length=1024, verbose_name="接口地址")
    headers = models.JSONField(verbose_name="请求头", blank=True, null=True)
    request_method = models.CharField(max_length=20, choices=REQUEST_METHOD_CHOICES, verbose_name="请求方式") 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="状态")
    request_params = models.JSONField(verbose_name="入参", blank=True, null=True)
    response_params = models.JSONField(verbose_name="出参", blank=True, null=True)
    desc = models.TextField('简要描述', max_length=2000)
    created_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, verbose_name="创建人")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口管理'
        verbose_name_plural = '接口管理表'