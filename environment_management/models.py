from django.db import models
from user_management.models import Users

# Create your models here.
class Environment(models.Model):
    id = models.AutoField(primary_key=True)
    environment_name = models.CharField(max_length=100, verbose_name="环境名称")
    environment_value = models.URLField(max_length=200, verbose_name="环境地址")
    description = models.TextField(verbose_name="描述", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, verbose_name="创建人")

    def __str__(self):
        return self.environment_name
    
    class Meta:
        verbose_name = '环境配置表'
        verbose_name_plural = '环境配置表'