from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Module
from .forms import ModuleForm
from django.core.paginator import Paginator
from .models import Project  
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


@login_required
def module_list(request):
    project_id = request.GET.get('project_id')
    if project_id:
        modules = Module.objects.filter(belong_project_id=project_id)
    else:
        modules = Module.objects.all()
    projects = Project.objects.all()
    # 分页设置  
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
        if per_page <= 0:
            per_page = 10
    except ValueError:
        per_page = 10

    # 分页设置，使用处理后的每页显示条数
    paginator = Paginator(modules, per_page)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    modules_page = paginator.get_page(page_number)

    # 构建可供选择的每页条数选项列表，这里示例为[5, 10, 15, 20]，可根据需求修改
    per_page_options = [5, 10, 15, 20]

    return render(request, 'modules/module_list.html', {'modules': modules_page, 'projects': projects, 'paginator': paginator,'per_page': per_page,
        'per_page_options': per_page_options})

@login_required
def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    return render(request, 'modules/module_detail.html', {'module': module})

@login_required
def module_search(request):
    query = request.POST.get('q', '')
    if query:
        modules = Module.objects.filter(name__icontains=query) | Module.objects.filter(test_owner__icontains=query)
    else:
        modules = Module.objects.all()

    paginator = Paginator(modules, 10)  # Show 10 modules per page.
    page_number = request.GET.get('page')
    modules_page = paginator.get_page(page_number)
    projects = Project.objects.all()
    return render(request, 'modules/module_list.html', {'modules': modules_page, 'paginator': paginator, 'projects': projects})

@login_required
def module_create(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('module_list')
    else:
        form = ModuleForm()
    return render(request, 'modules/module_form.html', {'form': form})

@login_required
def module_update(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('module_list')
    else:
        form = ModuleForm(instance=module)
    return render(request, 'modules/module_form.html', {'form': form})

@login_required
@require_POST
def module_delete(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    module.delete()
    return JsonResponse({'message': '删除成功'})