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

    path('modules/', views.module_list, name='module_list'),
    path('modules/<int:module_id>/', views.module_detail, name='module_detail'),
    path('modules/add/', views.module_create, name='module_create'),
    path('modules/<int:module_id>/edit/', views.module_update, name='module_update'),
    path('modules/search/', views.module_search, name='module_search'),

]
