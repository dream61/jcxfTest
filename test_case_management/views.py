from django.shortcuts import render
import requests,json

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import TestCase
from .forms import TestCaseForm
from api_management.models import ApiInterface
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import logging
from django.contrib.auth.decorators import login_required

@login_required
def testcase_list(request):
    query = request.GET.get('q')
    if query:
        testcases = TestCase.objects.filter(name__icontains=query)
    else:
        testcases = TestCase.objects.all()
    # 分页设置  
    paginator = Paginator(testcases, 10)  # 每页显示10个项目
    page_number = request.GET.get('page')
    testcases_page = paginator.get_page(page_number)

    return render(request, 'testcases/testcase_list.html', {'testcases': testcases_page,'paginator': paginator})

@login_required
def testcase_detail(request, testcase_id):
    testcase = get_object_or_404(TestCase, id=testcase_id)
    return render(request, 'testcases/testcase_detail.html', {'testcase': testcase})

@login_required
def testcase_search(request):
    query = request.GET.get('q')
    testcases = TestCase.objects.filter(name__icontains=query) if query else TestCase.objects.all()
    # 分页设置  
    paginator = Paginator(testcases, 10)  # 假设每页显示10个项目  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    return render(request, 'testcases/testcase_list.html', {'testcases': page_obj, 'query': query})

@login_required
def testcase_create(request):
    if request.method == 'POST':
        form = TestCaseForm(request.POST)
        if form.is_valid():
            testcase = form.save(commit=False)
            testcase.created_by = request.user
            form.save()
            return redirect('testcase_list')
    else:
        form = TestCaseForm()
    interfaces = ApiInterface.objects.all()
 
    return render(request, 'testcases/testcase_form.html', {'form': form, 'interfaces': interfaces})

@login_required
def testcase_update2(request, testcase_id):
    testcase = get_object_or_404(TestCase, id=testcase_id)
    if request.method == 'POST':
        form = TestCaseForm(request.POST, instance=testcase)
        if form.is_valid():
            form.save()
            return redirect('testcase_list')
    else:
        form = TestCaseForm(instance=testcase)
    return render(request, 'testcases/testcase_form.html', {'form': form})

@login_required
def testcase_update(request, testcase_id):
    testcase = get_object_or_404(TestCase, id=testcase_id)
    if request.method == 'POST':
        form = TestCaseForm(request.POST, instance=testcase)
        if form.is_valid():
             
            testcase = form.save()
            # 检查是否点击了运行按钮
            if 'run_case' in request.POST:
                # 运行测试用例的逻辑
                result = run_test_case_logic(testcase)
                return render(request, 'testcases/testcase_form.html', {'form': form, 'result': result})
            return redirect('testcase_list')
    else:
        form = TestCaseForm(instance=testcase)
    return render(request, 'testcases/testcase_form.html', {'form': form})


@require_POST
def testcase_delete(request, testcase_id):
    testcase = get_object_or_404(TestCase, pk=testcase_id)
    testcase.delete()
    return JsonResponse({'message': '删除成功'})

@login_required
def get_interface_details(request, interface_id):
    api_interface = ApiInterface.objects.get(id=interface_id)
    data = {
        'project': api_interface.project.name,  # 获取项目名称
        'module': api_interface.module.name,  # 获取模块名称
    }
    return JsonResponse(data)


def execute_test_case(request, case_id):
    test_case = get_object_or_404(TestCase, pk=case_id)
    url = test_case.host_url.environment_value+test_case.url

    try:
        # 根据请求方法选择参数传递的方式
        if test_case.request_method.upper() == 'GET':
            response = requests.get(url, params=test_case.request_data)
        elif test_case.request_method.upper() == 'POST':
            # POST 请求使用 json 参数，除非明确使用 form-data 等
            response = requests.post(url, json=json.loads(test_case.body))
        elif test_case.request_method.upper() == 'PUT':
            response = requests.put(url, json=json.loads(test_case.body))
        elif test_case.request_method.upper() == 'DELETE':
            response = requests.delete(url, params=test_case.request_data)
        elif test_case.request_method.upper() == 'PATCH':
            response = requests.patch(url, json=json.loads(test_case.body))
        elif test_case.request_method.upper() == 'HEAD':
            response = requests.head(url, params=test_case.request_data)
        elif test_case.request_method.upper() == 'OPTIONS':
            response = requests.options(url, params=test_case.request_data)
        else:
            test_case.execute_result = "未知请求方法"
            test_case.save()
            return redirect('testcase_detail', case_id)
        
        # 比较实际结果与预期结果
        
        response_json = json.loads(response.text) if response.text else {}
        if response_json == test_case.expected_response:
            test_case.is_executed = True
            test_case.execute_result = "成功"
        else:
            test_case.execute_result = "失败"

        test_case.save()

    except Exception as e:
        # 处理异常情况
        print(f"Error: {e}")
        test_case.execute_result = "异常"
        test_case.save()

    return redirect('testcase_detail', case_id)

def run_test_case_logic(testcase):
    url = testcase.host_url.environment_value+testcase.url
    
    try:
        # 根据请求方法执行对应的HTTP请求
        if testcase.request_method.upper() == 'GET':   
            response = requests.get(url, params=testcase.request_data, headers=testcase.headers)
        elif testcase.request_method.upper() == 'POST':
            response = requests.post(url, json=json.loads(testcase.body))
        # 其他方法类似...
        elif testcase.request_method.upper() == 'PUT':
            response = requests.put(url, json=json.loads(testcase.body))
        elif testcase.request_method.upper() == 'DELETE':
            response = requests.delete(url, params=testcase.request_data)
        elif testcase.request_method.upper() == 'PATCH':
            response = requests.patch(url, json=json.loads(testcase.body))
        elif testcase.request_method.upper() == 'HEAD':
            response = requests.head(url, params=testcase.request_data)
        elif testcase.request_method.upper() == 'OPTIONS':
            response = requests.options(url, params=testcase.request_data)
        else:
            testcase.execute_result = "未知请求方法"
            testcase.save()
        
        # 比较实际结果和预期结果
        response_json = response.json() if response.text else {}
        if response_json == testcase.expected_response:
            testcase.is_executed = True
            testcase.execute_result = "成功"
            testcase.save()
            return "测试成功，结果符合预期"
        else:
            testcase.execute_result = "失败"
            testcase.save()
            return f"测试失败，实际结果: {response_json}"
        

    except Exception as e:
        testcase.execute_result = "异常"
        testcase.save()
        return f"测试执行异常: {e}"

    
  
