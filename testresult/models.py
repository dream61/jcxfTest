from django.db import models
from testscenario.models import TestScenario
from user_management.models import Users

# Create your models here.
class TestResult(models.Model):
    id = models.AutoField(primary_key=True)
    scenario = models.ForeignKey(TestScenario, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=(('success', '成功'), ('fail', '失败'), ('running', '运行中')))
    execution_time = models.DateTimeField(auto_now_add=True)
    executed_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    report_file = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '测试结果表'
        verbose_name_plural = '测试结果表'
   