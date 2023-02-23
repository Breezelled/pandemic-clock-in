"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from . import views

app_name = 'adminuser'

urlpatterns = [
    # path('index/', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login', views.admin_login, name='login'),
    path('update', views.admin_update, name='update'),
    path('navi_statistics', views.navi_statistics, name='navi_statistics'),
    path('statistics', views.statistics, name='statistics'),
    path('not_clockin_rank', views.not_clockin_rank, name='not_clockin_rank'),
    path('export_excel', views.export_excel, name='export_excel')
]
