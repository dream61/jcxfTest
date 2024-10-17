from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project_management.models import Project
from module_management.models import Module
from api_management.models import ApiInterface
from test_case_management.models import TestCase
from testresult.models import TestResult
from django.contrib.auth.decorators import login_required

@login_required
def home(request):  
    project_count=Project.objects.all().count
    module_count=Module.objects.all().count
    interface_count=ApiInterface.objects.all().count
    testcase_count=TestCase.objects.all().count
    recent_report=TestResult.objects.latest('execution_time')
    report_time=recent_report.execution_time
    STATUS_CHOICES = {  
        'success': '通过',  
        'fail': '失败',  
        'running': '运行中',  
      
    } 
    report_status = STATUS_CHOICES.get(recent_report.status, '未知状态') if recent_report else '无最近报告'
    #report_status=recent_report.status
    
    context = {
        'project_count': project_count,  # 例如，项目的数量
        'module_count': module_count,    # 模块的数量
        'interface_count':interface_count,
        'testcase_count': testcase_count,  # 测试用例的数量
        'report_time': report_time,
        'report_status': report_status,
        
    }
    return render(request, 'home.html', context)