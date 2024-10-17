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
from django.urls import path
from . import views

urlpatterns = [

    path('testcases/', views.testcase_list, name='testcase_list'),
    path('testcases/<int:testcase_id>/', views.testcase_detail, name='testcase_detail'),
    path('testcases/add/', views.testcase_create, name='testcase_create'),
    path('testcases/<int:testcase_id>/edit/', views.testcase_update, name='testcase_update'),
    path('testcases/search/', views.testcase_search, name='testcase_search'),
    
     

]
