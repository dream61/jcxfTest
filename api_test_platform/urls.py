"""api_test_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from environment_management.views import environment_delete
from project_management.views import project_delete
from module_management.views import module_delete
from user_management import views
from api_management.views import get_modules_by_project,interface_delete
from test_case_management.views import execute_test_case,get_interface_details,testcase_delete
from testscenario.views import add_test_case_to_scenario,testscenior_delete,save_testcases,run_scenario,test_results
from testresult.views import testresult_delete
from scheduled_tasks.views import scheduled_delete,run_scheduled





urlpatterns = [
    #path('admin/', admin.site.urls),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('', include('home.urls')),
    path('environments/', include('environment_management.urls')),
    path('environments/<int:environment_id>/delete/', environment_delete, name='environment_delete'),
    path('projects/', include('project_management.urls')),
    path('projects/<int:project_id>/delete/', project_delete, name='project_delete'),
    path('modules/', include('module_management.urls')),
    path('modules/<int:module_id>/delete/', module_delete, name='module_delete'),
    path('interfaces/', include('api_management.urls')),
    path('interfaces/<int:interface_id>/delete/', interface_delete, name='interface_delete'),
    path('get_modules/<int:project_id>/', get_modules_by_project, name='get_modules_by_project'),
    path('testcases/', include('test_case_management.urls')),
    path('testcases/<int:testcase_id>/delete/', testcase_delete, name='testcase_delete'),
    path('execute/<int:case_id>/', execute_test_case, name='execute_test_case'), 
    path('api/interface/<int:interface_id>/', get_interface_details, name='get_interface_details'),
    path('testscenarios/', include('testscenario.urls')),
    path('testscenarios/<int:testscenario_id>/delete/', testscenior_delete, name='testscenior_delete'),
    path('testscenarios/<int:testscenario_id>/add_testcases/', add_test_case_to_scenario, name='add_testcases_to_scenario'),
    path('testscenarios/<int:testscenario_id>/save_testcases/', save_testcases, name='save_testcases'),
    path('run_scenario/<int:testscenario_id>/', run_scenario, name='run_scenario'),
    path('test_results/', test_results, name='test_results'),
    path('testresults/',include('testresult.urls')),
    path('testresults/<int:result_id>/delete/', testresult_delete, name='testresult_delete'),
    path('users/',include('user_management.urls')),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('scheduledes/',include('scheduled_tasks.urls')),
    path('scheduledes/delete/<int:scheduled_id>/', scheduled_delete, name='scheduled_delete'),
    path('run_scheduled/<int:scheduled_id>/', run_scheduled, name='run_scheduled'),
   
]
