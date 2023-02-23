from django import template
import datetime

register = template.Library()


@register.simple_tag
def time_format(time):
    f = '%Y年%m月%d日 %H:%M'
    return datetime.datetime.strftime(time, f)
