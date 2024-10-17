from django.db import models
from test_case_management.models import TestCase
from user_management.models import Users

# Create your models here.
class TestScenario(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,verbose_name="场景名称")
    description = models.TextField(blank=True, null=True,verbose_name="描述")
    test_cases = models.ManyToManyField(TestCase, related_name='scenarios',verbose_name="测试用例")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, verbose_name="创建人")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '测试场景表'
        verbose_name_plural = '测试场景表'
