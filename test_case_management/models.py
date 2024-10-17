from django.db import models

# Create your models here.
from django.db import models
from api_management.models import ApiInterface
from user_management.models import Users
from environment_management.models import Environment


class TestCase(models.Model):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
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
    id = models.AutoField(primary_key=True)
    relate_api = models.ForeignKey(ApiInterface, on_delete=models.CASCADE, verbose_name="关联接口")
    name = models.CharField(max_length=255,verbose_name="测试用例名称")
    request_method = models.CharField(max_length=20, choices=REQUEST_METHOD_CHOICES, verbose_name="请求方法")
    host_url = models.ForeignKey(Environment, on_delete=models.CASCADE, verbose_name="host地址") 
    url =models.CharField(max_length=1024, verbose_name="接口地址")
    headers = models.JSONField(verbose_name="请求头", blank=True,null=True)
    body = models.TextField(blank=True, verbose_name="Request Body")
    description = models.TextField(verbose_name="描述", blank=True,null=True)
    request_data = models.JSONField(verbose_name="请求参数")
    expected_response = models.JSONField(verbose_name="期望结果")
    extract_var = models.CharField('关联参数', max_length=1024, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, verbose_name="创建人")
    status = models.IntegerField(null=True, help_text="0:表示有效，1:表示无效")
    is_executed = models.BooleanField(default=False, verbose_name="是否执行")
    is_smoke = models.BooleanField(default=False, verbose_name="是否冒烟")
    is_reback = models.BooleanField(default=False, verbose_name="是否回归")
    execute_result = models.CharField('执行结果', max_length=1024, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '测试用例表'
        verbose_name_plural = '测试用例表'
