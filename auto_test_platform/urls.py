"""auto_test_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from 测试计划 import views as plan_views

urlpatterns = [
    path('index/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('dump/', plan_views.dump, name='dump'),
    path('dump_checkbox/', plan_views.dump_checkbox, name='dump_checkbox'),
    path('', plan_views.plans, name='plans'),
    path('plans/', plan_views.plans, name='plans'),
    path('add_plan/', plan_views.add_plan, name='add_plan'),
    path('update_plan/<id>/', plan_views.update_plan, name='update_plan'),
    path('delete_plan/<id>/', plan_views.delete_plan, name='delete_plan'),
    path('exec/<id>/', plan_views.exec, name='exec'),
    path('history_report/<id>/', plan_views.history_report, name='history_report'),
    path('download_report/<report_id>/', plan_views.download_report, name='download_report'),
    path('delete_report/<report_id>/', plan_views.delete_report, name='delete_report'),

]
