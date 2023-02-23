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
from .views import *
from . import views

app_name = 'login'

urlpatterns = [
    path('index/', views.index, name="index"),
    path("register/", views.register, name="register"),
    path('user_detail/', views.user_detail, name="user_detail"),
    path('user_update/', views.user_update, name="user_update"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_delete/<str:user_uuid>', views.user_delete, name='user_delete'),
    re_path('^user_update/get_all_org/', views.get_all_org, name='get_all_org'),
    path('is_have_email', views.is_have_email, name='is_have_email'),
    path('check_pwd', views.check_pwd, name='check_pwd'),
    path('user_login/pc_get_captcha', views.pc_get_captcha, name='pc_get_captcha'),
    path('register/pc_get_captcha', views.pc_get_captcha, name='pc_get_captcha'),
    path('page_not_found_error', views.page_not_found_error, name='page_not_found_error'),
    path('page_error', views.page_error, name='page_error')
]
