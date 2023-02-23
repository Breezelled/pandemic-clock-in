import datetime, json, os, time, uuid
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from login.models import User
from .models import Admin, Org
from clockin.models import Record
from .forms import AdminRegisterForm, AdminUpdateForm, AdminLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from notifications.signals import notify
from apscheduler.scheduler import Scheduler
from functools import cmp_to_key
from django.views.decorators.clickjacking import xframe_options_sameorigin
from pyecharts.globals import CurrentConfig, ThemeType
from pyecharts import options as opts
from pyecharts.charts import Pie
from django.contrib import messages
from notifications.models import Notification
from xlwt import Workbook
from io import BytesIO


@xframe_options_sameorigin
@login_required(login_url='/login/user_login/')
def statistics(request):
    org = User.objects.get(user_uuid=request.session['user_uuid']).user_org
    org_people_num = User.objects.exclude(is_superuser=1).filter(user_org=org).count()
    org_people = User.objects.filter(user_org=org)
    statis_type = request.GET.get('type')
    exact_figure, cut_num = 0, 0
    anticipate_figure = 0
    title = ""
    if statis_type == 'day':
        anticipate_figure = org_people_num
        cut_num = 1
        title = "日"
    elif statis_type == 'week':
        anticipate_figure = 7 * org_people_num
        cut_num = 7
        title = "周"
    elif statis_type == 'month':
        anticipate_figure = 30 * org_people_num
        cut_num = 30
        title = "月"
    day = datetime.datetime.now()
    for p in org_people:
        exact = Record.objects.filter(user_id=p.user_uuid).all().order_by('-create_time')[:cut_num]
        exact_figure += len(exact)
    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT)).add("", list(zip(['已打卡', '未打卡'],
                                                                             [exact_figure,
                                                                              anticipate_figure - exact_figure])))
            .set_global_opts(title_opts=opts.TitleOpts()).set_series_opts(
            label_opts=opts.LabelOpts(formatter="{b}:{c}\n({d}%)"))
    )
    data = {'data': pie.render_embed()}
    return render(request, 'chart.html', data)


def navi_statistics(request):
    return render(request, 'adminuser/statistics.html')


# Create your views here.
def register(request):
    # 不是超级管理员 不允许进入创建管理员界面
    if request.session['admin_level'] is None or request.session['admin_level'] != 1:
        return redirect("login:index")
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        user_register_form = AdminRegisterForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.is_superuser = 1;
            # 随机生成uuid
            new_user.user_uuid = uuid.uuid1()
            new_user.save()
            new_user = authenticate(email=new_user.email, password=user_register_form.cleaned_data['password'])
            admin = Admin()
            admin.admin_name = new_user.user_name
            admin.admin_id = new_user.user_uuid
            admin.admin_level = 2
            admin.admin_org = new_user.user_org
            admin.save()
            login(request, new_user)
            request.session['user_uuid'] = new_user.user_uuid
            request.session['admin_level'] = admin.admin_level
            return redirect("login:index")
        # 如果数据不合法，返回错误信息
        else:
            print(user_register_form.errors)
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    elif request.method == 'GET':
        # 创建表单类实例
        user_register_form = AdminRegisterForm()
        # 赋值上下文
        context = {'user_form': user_register_form}
        # 返回模板
        return render(request, 'adminuser/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def admin_login(request):
    if request.method == 'POST':
        user_form = AdminLoginForm(data=request.POST)
        if user_form.is_valid():
            data = user_form.cleaned_data
            user = authenticate(email=data['email'], password=data['password'])
            if user:
                if user.is_superuser == 0:
                    messages.error(request, '没有此管理员')
                    return redirect('login:user_login')
                admin = Admin.objects.get(admin_id=user.user_uuid)
                request.session['user_uuid'] = user.user_uuid
                request.session['admin_level'] = admin.admin_level
                if admin.admin_level > 1:
                    if Org.objects.get(org_name=admin.admin_org).strategy_time is not None and Org.objects.get(
                            org_name=admin.admin_org).strategy_time != '':
                        request.session['strategy_time'] = str(Org.objects.get(org_name=admin.admin_org).strategy_time)
                        print(request.session['strategy_time'])
                    else:
                        request.session['strategy_time'] = ''
                login(request, user)
                return redirect("login:index")
            else:
                messages.error(request, '账号或密码输入有误，请重新输入')
                return redirect('login:user_login')
        else:
            messages.error(request, '账号或密码输入不合法')
            return redirect('login:user_login')
    elif request.method == 'GET':
        user_form = AdminLoginForm()
        context = {'user_form': user_form}
        return render(request, 'user/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


@login_required(login_url='/login/user_login/')
def admin_update(request):
    user = User.objects.get(user_uuid=request.session['user_uuid'])
    admin = Admin.objects.get(admin_id=request.session['user_uuid'])
    photo = user.profile_photo.path
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        user_form = AdminUpdateForm(request.POST, request.FILES, instance=user)
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
            # if request.POST['strategy_time'] == '' or request.POST['strategy_time'] is None:
            # admin.
            user.save()
            org = Org.objects.get(org_name=admin.admin_org)

            if request.POST['strategy_time'] is not None and request.POST['strategy_time'] != '':
                org.strategy_time = request.POST['strategy_time']
                request.session['strategy_time'] = org.strategy_time
            else:
                request.session['strategy_time'] = ''

            org.save()
            # 完成后返回到用户明细
            return redirect("login:user_detail")
        # 如果数据不合法，返回错误信息
        else:
            print(user_form.errors)
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        user_update_form = AdminUpdateForm()
        # 赋值上下文
        context = {'user': user, 'user_update_form': user_update_form}
        # 返回模板
        return render(request, 'user/update.html', context)


# 实例化定时任务
sched = Scheduler()


# 每日自动打卡提醒
@sched.interval_schedule(minutes=1, coalesce=False)
def remind_clockin():
    now = datetime.datetime.now()
    cur = datetime.datetime.strftime(now, "%H:%M")
    day = datetime.datetime.strftime(now, "%Y-%m-%d")
    orgs = list(Org.objects.exclude(strategy_time=None).filter(strategy_time=cur))
    print(orgs)
    if len(orgs) == 0:
        return
    for org in orgs:
        admin = Admin.objects.get(admin_org=org.org_name)
        users = list(User.objects.exclude(user_uuid=admin.admin_id).filter(user_org=admin.admin_org))
        for user in users:
            if Record.objects.filter(user_id=user.user_uuid).filter(create_time=day).count() == 0:
                print(user)
                notify.send(admin, recipient=user, verb='通知你该打卡了')

        print(users)

    print("_____________________test_____________________")
    # admins = Admin.objects.exclude(admin_level=1).all().first()
    # print(admins)
    # user = User.objects.get(user_id=3)
    # notify.send(admins, recipient=user, verb='通知你该打卡了')


sched.start()

excel_user = []


@login_required(login_url='/login/user_login/')
def not_clockin_rank(request):
    admin = Admin.objects.filter(admin_id=request.session['user_uuid']).first()
    org = admin.admin_org
    users = User.objects.filter(user_org=org).all()
    global excel_user
    excel_user = users
    rank = []
    for u in users:
        cnt = Notification.objects.filter(recipient_id=u.user_id)[:30].count()
        if cnt > 0:
            rank.append({'user': {'user_bind_num': u.user_bind_num, 'email': u.email, 'phone': u.phone,
                                  'realname': u.realname}, 'cnt': cnt})
    rank = {'data': rank}
    return JsonResponse(rank)


def export_excel(request):
    if len(excel_user) > 0:
        # 建立工做簿
        ws = Workbook(encoding='utf-8')
        # 添加第一页数据表
        w = ws.add_sheet(u"第一页")
        # 写入表头
        w.write(0, 0, u'姓名')
        w.write(0, 1, u'学号')
        w.write(0, 2, u'邮箱')
        w.write(0, 3, u'手机')
        # 写入数据
        excel_row = 1
        for obj in excel_user:
            name = obj.realname
            sno = obj.user_bind_num
            email = obj.email
            phone = obj.phone
            # 写入每一行对应的数据
            w.write(excel_row, 0, name)
            w.write(excel_row, 1, sno)
            w.write(excel_row, 2, email)
            w.write(excel_row, 3, phone)
            excel_row += 1
        # 实现下载
        output = BytesIO()
        ws.save(output)
        output.seek(0)
        response = StreamingHttpResponse(output)
        response['content_type'] = 'application/vnd.ms-excel'
        response['charset'] = 'utf-8'
        response['Content-Disposition'] = 'attachment; filename="{0}.xls"'.format(
            datetime.datetime.now().strftime('%Y%m%d%H%M'))
        return response
