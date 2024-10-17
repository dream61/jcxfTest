from django.db import models
from testresult.models import TestResult

# Create your models here.
class TestReport(models.Model):
    id = models.AutoField(primary_key=True)
    test_result = models.OneToOneField(TestResult, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='reports/')
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '测试报告表'
        verbose_name_plural = '测试报告表'

