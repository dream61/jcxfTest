from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from scheduled_tasks.models import ScheduledTask
from user_management.models import Users
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage 
from .forms import ScheduledTaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from api_test_platform.task import run_scheduled_task
from testresult.models import TestResult
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json


@login_required
def scheduled_list(request):
    query = request.GET.get('q')
    if query:
        scheduledes = ScheduledTask.objects.filter(name__icontains=query)
    else:
        scheduledes = ScheduledTask.objects.all()

    # 分页设置  
    paginator = Paginator(scheduledes, 10)  # 每页显示10个项目
    page_number = request.GET.get('page')
    scheduled_page = paginator.get_page(page_number)
    return render(request, 'scheduledes/scheduledes_list.html', {'scheduledes': scheduled_page,'paginator': paginator})

@login_required
def scheduled_search(request):
    query = request.GET.get('q')
    scheduledes = ScheduledTask.objects.filter(name__icontains=query) if query else ScheduledTask.objects.all()
    # 分页设置  
    paginator = Paginator(scheduledes, 10)  # 假设每页显示10个项目  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    return render(request, 'scheduledes/scheduledes_list.html', {'scheduledes': page_obj, 'query': query})

@login_required
def scheduled_create(request):
    if request.method == 'POST':
        form = ScheduledTaskForm(request.POST)
        if form.is_valid():
            sceheduled = form.save(commit=False)
            sceheduled.created_by = request.user
            sceheduled.status = 'pendding'
            sceheduled.save()
            messages.success(request, '定时任务添加成功！')
            return redirect('scheduled_list')
    else:
        form = ScheduledTaskForm()
    return render(request, 'scheduledes/scheduled_form.html', {'form': form})

@login_required
def scheduled_update(request, scheduled_id):
    scheduled = get_object_or_404(ScheduledTask, pk=scheduled_id)
    if request.method == 'POST':
        form = ScheduledTaskForm(request.POST, instance=scheduled)
        if form.is_valid():
            form.save()
            messages.success(request, '定时任务修改成功！')
            return redirect('scheduled_list')
    else:
        form = ScheduledTaskForm(instance=scheduled)
    return render(request, 'scheduledes/scheduled_form.html', {'form': form})

@require_POST
def scheduled_delete(request, scheduled_id):
    scheduled = get_object_or_404(ScheduledTask, pk=scheduled_id)
    scheduled.delete()
    return JsonResponse({'message': '删除成功'})

@login_required
def run_scheduled(request,scheduled_id):
    if request.method == 'POST':
        scheduled = get_object_or_404(ScheduledTask, id=scheduled_id)

        # 创建测试结果记录
        test_result = TestResult.objects.create(
            scenario=scheduled.testscenario,
            status='running',
            executed_by=request.user
        )

        # 调用Celery任务
        run_scheduled_task.delay(test_result.id)

        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'fail'}, status=400)

def schedule_task(task):
    # 创建 Cron 表达式
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute=task.cron_expression.minute,
        hour=task.cron_expression.hour,
        day_of_week=task.cron_expression.day_of_week,
        day_of_month=task.cron_expression.day_of_month,
        month_of_year=task.cron_expression.month_of_year,
    )
    # 创建 Celery 周期性任务
    PeriodicTask.objects.create(
        crontab=schedule,
        name=f"Execute task {task.id}",
        task='api_test_platform.tasks.run_scheduled_task',
        args=json.dumps([task.id])
    )