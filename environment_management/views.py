from django.shortcuts import render, get_object_or_404, redirect
from .models import Environment
from .forms import EnvironmentForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
def environment_list(request):
    query = request.GET.get('q')
    if query:
        environments = Environment.objects.filter(environment_name__icontains=query)
    else:
        environments = Environment.objects.all()
    # 分页设置  
    paginator = Paginator(environments, 10)  # 每页显示10个项目
    page_number = request.GET.get('page')
    environments_page = paginator.get_page(page_number)

    return render(request, 'environments/environment_list.html', {'environments': environments_page, 'paginator': paginator})

@login_required
def environment_search(request):
    query = request.GET.get('q')
    environments = Environment.objects.filter(environment_name__icontains=query) if query else Environment.objects.all()
    # 分页设置  
    paginator = Paginator(environments, 10)  # 假设每页显示10个项目  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    return render(request, 'environments/environment_list.html', {'environments': environments, 'query': query})

@login_required
def environment_create(request):
    if request.method == 'POST':
        form = EnvironmentForm(request.POST)
        if form.is_valid():
            environment = form.save(commit=False)
            environment.created_by = request.user
            form.save()
            messages.success(request, '环境添加成功！')
            return redirect('environment_list')
    else:
        form = EnvironmentForm()
    return render(request, 'environments/environment_form.html', {'form': form})

@login_required
def environment_update(request, environment_id):
    environment = get_object_or_404(Environment, id=environment_id)
    if request.method == 'POST':
        form = EnvironmentForm(request.POST, instance=environment)
        if form.is_valid():
            form.save()
            messages.success(request, '环境更新成功！')
            return redirect('environment_list')
    else:
        form = EnvironmentForm(instance=environment)
    return render(request, 'environments/environment_form.html', {'form': form})


@login_required
@require_POST
def environment_delete(request, environment_id):
    environment = get_object_or_404(Environment, pk=environment_id)
    environment.delete()
    return JsonResponse({'message': '删除成功'})
