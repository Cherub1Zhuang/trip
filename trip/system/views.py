import json

from django import http
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView

from system.forms import SendSmsCodeForm
from system.models import Slider
from utils.response import ServerErrorJsonResponse, BadRequestJsonResponse


def slider_list(request):
    """ 轮播图接口
    {
        "meta": {},
        "objects": []
    }
    """
    data = {
        'meta': {

        },
        'objects': []
    }
    queryset = Slider.objects.filter(is_valid=True)
    for item in queryset:
        data['objects'].append({
            'id': item.id,
            'img_url': item.img.url,
            'target_url': item.target_url,
            'name': item.name
        })
    # return HttpResponse(data)
    return http.JsonResponse(data)


def cache_set(request):
    """ 写缓存 """
    cache.set('username', 'lisi')
    # 5之后自动删除
    cache.set('password', 'password', timeout=5)
    return HttpResponse('ok')


def cache_get(request):
    """ 读缓存 """
    value = cache.get('username')
    return HttpResponse(value)

def send_sms(request):
    pass
    # 拿到手机号，判断是否为真实手机号
    # 生产验证码，并存储
    #调用短信的发生接口
    # 告诉验证码发送是否成功


class SmsCodeView(FormView):
    form_class = SendSmsCodeForm

    def form_valid(self, form):
        """表单已经通过验证"""
        data=form.send_sms_code()
        if data is not None:
            return http.JsonResponse(data,status=201)
        return ServerErrorJsonResponse()

    def form_invalid(self, form):
        """没有通过验证"""
        err_list=json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err_list)