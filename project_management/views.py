from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
def project_list(request):
    query = request.GET.get('q')
    if query:
        projects = Project.objects.filter(name__icontains=query) | Project.objects.filter(desc__icontains=query)
    else:
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
    paginator = Paginator(projects, per_page)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    projects_page = paginator.get_page(page_number)

    # 构建可供选择的每页条数选项列表，这里示例为[5, 10, 15, 20]，可根据需求修改
    per_page_options = [5, 10, 15, 20]

    return render(request, 'projects/project_list.html', {'projects': projects_page, 'paginator': paginator,'per_page': per_page,
        'per_page_options': per_page_options})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/project_detail.html', {'project': project})

@login_required
def project_search(request):
    query = request.GET.get('q')
    projects = Project.objects.filter(name__icontains=query) if query else Project.objects.all()
    # 分页设置  
    paginator = Paginator(projects, 10)  # 假设每页显示10个项目  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    return render(request, 'projects/project_list.html', {'projects': projects, 'query': query})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '项目添加成功！')
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, '项目更新成功！')
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form})


@login_required
@require_POST
def project_delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return JsonResponse({'message': '删除成功'})
