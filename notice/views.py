from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


# 继承ListView展示未读通知，访问前必须登录
class NoticeListView(LoginRequiredMixin, ListView):
    context_object_name = 'notices'
    template_name = 'notice/notice.html'
    login_url = '/login/user_login/'

    # 返回未读通知
    def get_queryset(self):
        return self.request.user.notifications.unread()


class NoticeUpdateView(View):
    def get(self, request):
        notice_id = request.GET.get('notice_id')
        # 已读单条通知
        if notice_id:
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect('clockin:daily_clockin')
        # 清空全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')
