from django.db import models
from testscenario.models import TestScenario

# Create your models here.
class TestPlan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    scenarios = models.ManyToManyField(TestScenario, related_name='plans')
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')  # Pending, Running, Completed

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '测试计划表'
        verbose_name_plural = '测试计划表'

