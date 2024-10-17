from django.shortcuts import render, get_object_or_404, redirect
from .models import TestResult
from test_reports.models import TestReport
from django.http import FileResponse, Http404,JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage 
import os
from django.contrib.auth.decorators import login_required

@login_required
def testresult_list(request):
    query = request.GET.get('q')
    if query:
        testresults = TestResult.objects.filter(scenario__name__icontains=query)
    else:
        testresults = TestResult.objects.all()

    # 分页设置  
    paginator = Paginator(testresults, 10)  # 每页显示10个项目
    page_number = request.GET.get('page')
    testresults_page = paginator.get_page(page_number)

    return render(request, 'testresults/testresult_list.html', {'testresults': testresults_page,'paginator': paginator})

@login_required
def testresult_search(request):
    query = request.GET.get('q')
    testresults = TestResult.objects.filter(scenario__name__icontains=query) if query else TestResult.objects.all()
    # 分页设置  
    paginator = Paginator(testresults, 10)  # 使用查询集进行分页  
    page_number = request.GET.get('page', 1)  # 如果没有提供 page，则默认为 1  
  
    try:  
        page_obj = paginator.get_page(page_number)  
    except PageNotAnInteger:  
        # 如果提供的页码不是整数，返回第一页。  
        page_obj = paginator.get_page(1)  
    except EmptyPage:  
        # 如果提供的页码超出页数，返回最后一页。  
        page_obj = paginator.get_page(paginator.num_pages)
    return render(request, 'testresults/testresult_list.html', {'testresults': page_obj, 'query': query})

@login_required
def download_report(request, result_id):
    try:
        # 根据 result_id 获取对应的 TestResult 实例
        test_result = TestResult.objects.get(id=result_id)
        file_path = test_result.report_file  # 获取报告文件路径
        
        if file_path and os.path.exists(file_path):
            # 返回报告文件
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        else:
            raise Http404("报告文件未找到")
    except TestResult.DoesNotExist:
        raise Http404("测试结果不存在")

@login_required    
@require_POST
def testresult_delete(request, result_id):
    result = get_object_or_404(TestResult, pk=result_id)
    result.delete()
    return JsonResponse({'message': '删除成功'})