import json
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from geetest import GeetestLib

from .models import User, Org
from .forms import UserRegisterForm, UserUpdateForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.conf import settings
from django.contrib import messages
import uuid
from PIL import Image

# Create your views here.

pc_geetest_id = "f55c61e3970995968513fe70d2379a02"  # id
pc_geetest_key = "a64ef3f8ee1a0fcc5fc0ede61a443392"  # key


def pc_get_captcha(request):
    # 极验验证函数
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def index(request):
    return render(request, "index.html")


def register(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        user_register_form = UserRegisterForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            # 随机生成uuid
            new_user.user_uuid = uuid.uuid1()
            new_user.save()
            new_user = authenticate(email=new_user.email, password=user_register_form.cleaned_data['password'])
            login(request, new_user)
            request.session['user_uuid'] = new_user.user_uuid
            return redirect("login:index")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    elif request.method == 'GET':
        # 创建表单类实例
        user_register_form = UserRegisterForm()
        # 赋值上下文
        context = {'user_form': user_register_form}
        # 返回模板
        return render(request, 'user/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


@login_required(login_url='/login/user_login/')
def user_detail(request):
    user = User.objects.get(user_uuid=request.session['user_uuid'])
    context = {"user": user}
    return render(request, "user/detail.html", context)


@login_required(login_url='/login/user_login/')
def user_update(request):
    user = User.objects.get(user_uuid=request.session['user_uuid'])
    photo = user.profile_photo.path
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        # 判断提交的数据是否满足模型的要求
        if user_form.is_valid():
            user.user_name = request.POST['user_name']
            user.user_org = request.POST['user_org']
            if request.POST['phone'] == '' or request.POST['phone'] is None:
                user.phone = None
            else:
                user.phone = request.POST['phone']
            user.email = request.POST['email']
            user.user_bind_num = request.POST['user_bind_num']
            try:
                user.gender = request.POST['gender']
            except MultiValueDictKeyError:
                user.gender = 2
            if 'profile_photo' in request.FILES:
                if photo != settings.MEDIA_ROOT + "default.png":
                    os.remove(photo)
                user.profile_photo = request.FILES['profile_photo']
            user.save()
            if user.user_org is not None and user.user_org.strip() != '':
                request.session['location'] = Org.objects.filter(org_name=user.user_org).first().org_designate_location
            # 完成后返回到用户明细
            return redirect("login:user_detail")
        # 如果数据不合法，返回错误信息
        else:
            print(user_form.errors)
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        user_update_form = UserUpdateForm()
        # 赋值上下文
        context = {'user': user, 'user_update_form': user_update_form}
        # 返回模板
        return render(request, 'user/update.html', context)


def user_login(request):
    if request.method == 'POST':
        user_form = UserLoginForm(data=request.POST)
        if user_form.is_valid():
            data = user_form.cleaned_data
            user = authenticate(email=data['email'], password=data['password'])
            if user:
                login(request, user)
                request.session['user_uuid'] = user.user_uuid
                request.session['location'] = Org.objects.filter(org_name=user.user_org).first().org_designate_location
                return redirect("login:index")
            else:
                messages.error(request, "账号或密码错误")
                return redirect("login:user_login")
        else:
            messages.error(request, "账号或密码错误")
            return redirect("login:user_login")
    elif request.method == 'GET':
        user_form = UserLoginForm()
        context = {'user_form': user_form}
        return render(request, 'user/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


@login_required(login_url='/login/user_login/')
def user_logout(request):
    logout(request)
    return redirect("login:index")


def get_all_org(request):
    org_list = Org.objects.all()
    org_list = serializers.serialize('json', org_list)
    return HttpResponse(org_list, content_type='application/json')


def is_have_email(request):
    val = request.POST.get('email')
    email = User.objects.filter(email=val).count()
    if email != 0:
        return HttpResponse(json.dumps(({'result': 'False'})))
    else:
        return HttpResponse(json.dumps(({'result': 'True'})))


def check_pwd(request):
    pwd1 = request.POST.get('pwd1')
    pwd2 = request.POST.get('pwd2')
    if str(pwd1) == str(pwd2):
        return HttpResponse(json.dumps(({'result': 'True'})))
    else:
        return HttpResponse(json.dumps(({'result': 'False'})))


@login_required(login_url='/login/user_login/')
def user_delete(request, user_uuid):
    if request.method == 'POST':
        user = User.objects.filter(user_uuid=user_uuid).first()
        # 验证登录用户、待删除用户是否相同
        if request.user == user:
            # 退出登录，删除数据
            logout(request)
            print(str(user))
            userUUID = str(user.user_uuid)
            print(userUUID)
            User.objects.get(user_uuid=userUUID).delete(using=User.objects.db)
            return redirect("login:index")
        else:
            return HttpResponse("你没有删除操作的权限。")
    else:
        return HttpResponse("仅接受post请求。")


def page_not_found_error(request, exception):
    return render(request, "index.html", context={'error': '访问有误:页面不存在'}, status=404)


def page_error(request):
    return render(request, "index.html", context={'error': '访问有误:服务器错误'}, status=500)
