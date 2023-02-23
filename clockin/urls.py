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

app_name = 'clockin'

urlpatterns = [
    # path('index/', views.index, name="index"),
    path('clockin_history', views.clockin_history, name="clockin_history"),
    path('daily_clockin', views.daily_clockin, name="daily_clockin"),
    path('is_clockin', views.is_clockin, name="is_clockin"),
    path('get_selection_data/<str:type>/<int:code>', views.get_selection_data, name='get_selection_data'),
]
