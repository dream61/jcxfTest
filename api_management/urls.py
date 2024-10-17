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

    path('interfaces/', views.interface_list, name='interface_list'),
    path('interfaces/<int:interface_id>/', views.interface_detail, name='interface_detail'),
    path('interfaces/add/', views.interface_create, name='interface_create'),
    path('interfaces/<int:interface_id>/edit/', views.interface_update, name='interface_update'),
    path('interfaces/search/', views.interface_search, name='interface_search'),

]
