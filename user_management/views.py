from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from user_management.models import UserManager, Users
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage 
from .form import UserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 成功登录后重定向到首页
        else:
            error_message = "用户名或密码不正确"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {'error': '密码不一致'})
        
        user = get_user_model().objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')

@login_required
def user_list(request):
    query = request.GET.get('q')
    if query:
        testresults = Users.objects.filter(username__icontains=query)
    else:
        testresults = Users.objects.all()

    # 分页设置  
    paginator = Paginator(testresults, 10)  # 每页显示10个项目
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    return render(request, 'users/users_list.html', {'users': users_page,'paginator': paginator})

@login_required
def user_search(request):
    query = request.GET.get('q')
    users = Users.objects.filter(username__icontains=query) if query else Users.objects.all()
    # 分页设置  
    paginator = Paginator(users, 10)  # 假设每页显示10个项目  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/users_list.html', {'users': page_obj, 'query': query})

@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '用户添加成功！')
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/create_user.html', {'form': form})

@login_required
def user_update(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, '用户修改成功！')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form})

@require_POST
def user_delete(request, user_id):
    scenario = get_object_or_404(Users, pk=user_id)
    scenario.delete()
    return JsonResponse({'message': '删除成功'})

@login_required
def user_logout(request):
    """处理用户退出逻辑"""
    logout(request)  # 调用Django自带的logout方法
    return redirect('login')  # 退出后重定向到登录页面