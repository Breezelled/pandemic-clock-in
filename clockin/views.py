import json
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Record, RecordInfo, Province, City, Area, Org
from .forms import RecordInfoForm
from adminuser.models import Admin
from login.models import User
from django.core import serializers
from django.contrib.auth.decorators import login_required
from models.models import Response
from django.contrib import messages
import datetime
from django.core.paginator import Paginator


@login_required(login_url='/login/user_login/')
def clockin_history(request):
    user = User.objects.get(user_uuid=request.session['user_uuid'])
    record_list = Record.objects.filter(user_id=request.session['user_uuid']).all().order_by('-create_time')[:14]
    paginator = Paginator(record_list, 3)
    page = request.GET.get('page')
    records = paginator.get_page(page)
    context = {'record_list': record_list, 'user': user, 'records': records}
    return render(request, 'clockin/clockin_history.html', context)


def is_clockin(request):
    user = User.objects.get(user_uuid=request.session['user_uuid'])
    if user.user_org is None or str(user.user_org).strip() == '':
        return HttpResponse(json.dumps(({'result': 'Org'})))
    day = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    if Record.objects.filter(user_id=user.user_uuid, create_time__startswith=day).count() > 0:
        return HttpResponse(json.dumps(({'result': 'False'})))
    else:
        return HttpResponse(json.dumps(({'result': 'True'})))


@login_required(login_url='/login/user_login/')
def daily_clockin(request):
    user = User.objects.get(user_uuid=request.session['user_uuid'])
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        record_info_form = RecordInfoForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if record_info_form.is_valid():
            record_info = record_info_form.save(commit=False)
            for s in request.POST.getlist('symptom_list'):
                record_info.symptom_list += s
            if request.POST['modify'] == '1':
                p = Province.objects.filter(code=record_info.address[0:2] + "0000").first().name
                c = City.objects.filter(code=record_info.address[0:4] + "00").first().name
                a = Area.objects.filter(code=record_info.address).first().name
                record_info.address = p + c + a
            record = Record()
            # 设置record唯一id
            record.record_id = uuid.uuid1()
            record_info.record_id = record.record_id
            record.ip = request.META.get('REMOTE_ADDR')
            record.user_id = user.user_uuid
            record.address = record_info.address
            record.designate_location = Org.objects.filter(org_name=user.user_org).first().org_designate_location
            record.create_time = datetime.datetime.now()
            record.save()
            record_info.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("login:index")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    else:
        if user.is_superuser == 0:
            # 创建表单类实例
            record_info_form = RecordInfoForm()
            context = {'record_form': record_info_form}
            # 将响应返回到模板中
            return render(request, 'clockin/daily_clockin.html', context)
        else:
            return HttpResponse("管理员")


# 获取三级联动查询数据
def get_selection_data(request, type, code):
    if type == "province":
        province = Province.objects.all()
        return Response.JsonResponse(province)
    elif type == "city":
        city = City.objects.filter(provincecode=code)
        return Response.JsonResponse(city)
    else:
        area = Area.objects.filter(citycode=code)
        return Response.JsonResponse(area)



