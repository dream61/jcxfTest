from django.db import models
from testscenario.models import TestScenario
from user_management.models import Users

class ScheduledTask(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="任务名称")
    testscenario = models.ForeignKey(TestScenario, on_delete=models.CASCADE, verbose_name="测试场景")
    cron_expression = models.CharField(max_length=100, verbose_name="CRON 表达式")
    email = models.EmailField(verbose_name="通知邮箱")
    status = models.CharField(max_length=50, choices=(('completed', '完成'),('pendding', '待运行'), ('failed', '失败'), ('running', '运行中'), ('stopping', '停止')),null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, verbose_name="创建人")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '定时任务表'
        verbose_name_plural = '定时任务表'
