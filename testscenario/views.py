from django.shortcuts import render
import requests,json
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import TestScenario
from .forms import TestSceniorForm
from test_case_management.models import TestCase
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib import messages
from api_test_platform.task import run_scenario_testcases
from testresult.models import TestResult
from django.contrib.auth.decorators import login_required


@login_required
def testscenario_list(request):
    query = request.GET.get('q')
    if query:
        testscenarios = TestScenario.objects.filter(name__icontains=query)
    else:
        testscenarios = TestScenario.objects.all()
        testcases = TestCase.objects.all()
    # 分页设置  
    paginator = Paginator(testscenarios, 10)  # 每页显示10个项目
    page_number = request.GET.get('page')
    testscenarios_page = paginator.get_page(page_number)

    return render(request, 'testscenarios/testscenario_list.html', {'testscenarios': testscenarios_page, 'testcases': testcases,'paginator': paginator})

@login_required
def testscenario_search(request):
    query = request.GET.get('q')
    testscenarios = TestScenario.objects.filter(name__icontains=query) if query else TestScenario.objects.all()
    # 分页设置  
    paginator = Paginator(testscenarios, 10)  # 假设每页显示10个项目  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    return render(request, 'testscenarios/testscenario_list.html', {'testscenarios': page_obj, 'query': query})

@login_required
def testscenario_create(request):
    if request.method == 'POST':
        form = TestSceniorForm(request.POST)
        if form.is_valid():
            scenario = form.save(commit=False)
            test_case_ids = request.POST.getlist('test_case_ids')  
            test_cases = TestCase.objects.filter(id__in=test_case_ids)  
            scenario.test_cases.set(test_cases) 
            scenario.created_by = request.user
            scenario.save()
            messages.success(request, '测试场景添加成功！')
            return redirect('testscenario_list')
    else:
        form = TestSceniorForm()
    return render(request, 'testscenarios/create_scenario.html', {'form': form})

@login_required
def testscenario_update(request, testscenario_id):
    scenario = get_object_or_404(TestScenario, pk=testscenario_id)
    if request.method == 'POST':
        form = TestSceniorForm(request.POST, instance=scenario)
        if form.is_valid():
            test_case_ids = request.POST.getlist('test_case_ids')  
            test_cases = TestCase.objects.filter(id__in=test_case_ids)  
            scenario.test_cases.set(test_cases) 
            form.save()
            messages.success(request, '测试场景修改成功！')
            return redirect('testscenario_list')
    else:
        form = TestSceniorForm(instance=scenario)
    return render(request, 'testscenarios/edit_scenario.html', {'form': form})

@require_POST
def testscenior_delete(request, testscenario_id):
    scenario = get_object_or_404(TestScenario, pk=testscenario_id)
    scenario.delete()
    return JsonResponse({'message': '删除成功'})

@login_required
def add_test_case_to_scenario(request, testscenario_id):
    scenario = get_object_or_404(TestScenario, id=testscenario_id)
    if request.method == 'POST':
        selected_cases = request.POST.getlist('selected_cases')
        if selected_cases:
            test_cases = TestCase.objects.filter(id__in=selected_cases)
            scenario.test_cases.add(*test_cases)  # 关联选中的测试用例
            messages.success(request, '测试用例添加成功！')
        else:
            messages.error(request, '未选择任何测试用例。')
    return redirect('testscenario_list')

@login_required
def save_testcases(request,testscenario_id):
    scenario = get_object_or_404(TestScenario, id=testscenario_id)
    if request.method == 'POST':
        selected_cases = request.POST.getlist('selected_cases')

        if selected_cases:
            test_cases = TestCase.objects.filter(id__in=selected_cases)
            scenario.test_cases.set(test_cases)
            scenario.save()
            messages.success(request, "测试用例保存成功")  # 添加成功提示
            return redirect('testscenario_list')  # 跳转到测试场景列表页
        else:
            # 返回错误消息，提示用户选择至少一个测试用例
            return JsonResponse({'error': '请选择至少一个测试用例'}, status=400)
    return render(request, 'testscenarios/testscenario_list.html', {'scenario': scenario})


# 运行测试场景，异步执行测试用例并生成报告
@login_required
def run_scenario(request,testscenario_id):
    if request.method == 'POST':
        scenario = get_object_or_404(TestScenario, id=testscenario_id)

        # 创建测试结果记录
        test_result = TestResult.objects.create(
            scenario=scenario,
            status='running',
            executed_by=request.user
        )

        # 调用Celery任务
        run_scenario_testcases.delay(test_result.id)

        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'fail'}, status=400)

@login_required    
def test_results(request):
    results = TestResult.objects.all().order_by('-execution_time')
    return render(request, 'testsresults/testresult_list.html', {'results': results})