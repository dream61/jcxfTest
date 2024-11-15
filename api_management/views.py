from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import ApiInterface, Module
from .forms import ApiForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def interface_list(request):
    query = request.GET.get('q')
    if query:
        apis = ApiInterface.objects.filter(name__icontains=query)
    else:
        apis = ApiInterface.objects.all()
    # 分页设置  
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
        if per_page <= 0:
            per_page = 10
    except ValueError:
        per_page = 10

    # 分页设置，使用处理后的每页显示条数
    paginator = Paginator(apis, per_page)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    apis_page = paginator.get_page(page_number)

    # 构建可供选择的每页条数选项列表，这里示例为[5, 10, 15, 20]，可根据需求修改
    per_page_options = [5, 10, 15, 20]

    return render(request, 'API/interface_list.html', {'apis': apis_page,'paginator': paginator,'per_page': per_page,
        'per_page_options': per_page_options})

@login_required
def interface_detail(request, interface_id):
    interface = get_object_or_404(ApiInterface, id=interface_id)
    return render(request, 'API/interface_detail.html', {'interface': interface})

@login_required
def interface_search(request):
    query = request.GET.get('q')
    apis = ApiInterface.objects.filter(name__icontains=query) if query else ApiInterface.objects.all()
    # 分页设置  
    paginator = Paginator(apis, 10)  # 假设每页显示10个项目  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    return render(request, 'API/interface_list.html', {'apis': page_obj, 'query': query})

@login_required
def interface_create(request):
    if request.method == 'POST':
        form = ApiForm(request.POST)
        if form.is_valid():
            interface = form.save(commit=False)
            interface.created_by = request.user
            form.save()
            messages.success(request, '接口添加成功！')
            return redirect('interface_list')
    else:
        form = ApiForm()
    return render(request, 'API/interface_form.html', {'form': form})

@login_required
def interface_update(request, interface_id):
    interface = get_object_or_404(ApiInterface, id=interface_id)
    if request.method == 'POST':
        form = ApiForm(request.POST, instance=interface)
        if form.is_valid():
            form.save()
            messages.success(request, '接口修改成功！')
            return redirect('interface_list')
    else:
        form = ApiForm(instance=interface)
    return render(request, 'API/interface_form.html', {'form': form})


@require_POST
def interface_delete(request, interface_id):
    interface = get_object_or_404(ApiInterface, pk=interface_id)
    interface.delete()
    return JsonResponse({'message': '删除成功'})

@login_required
def get_modules_by_project(request, project_id):
    # 获取与项目ID相关联的模块
    modules = Module.objects.filter(belong_project=project_id).values('id', 'name')
    return JsonResponse({'modules': list(modules)})

