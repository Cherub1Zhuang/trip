import json

from django import http
from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView
from django.views.generic.detail import BaseDetailView

import order.models
from order.choices import OrderStatus
from order.models import Order
from order.forms import SubmitTicketOrderForm
from order.serializers import OrderDetailSerializer, OrderListSeralizer
from utils.response import BadRequestJsonResponse, NotFoundJsonResponse
from utils.views import login_required


def ticket_submit(request):
    # 验证用户是否登录
    # 1获取post数据
    # 2数据验证（手机号 门票 库存）
    # 3关联用户 生产订单号 计算总价 生产订单
    # 4返回内容 订单id
    pass

@method_decorator(login_required, name='dispatch')
class TicketOrderSubmitView(FormView):
    """门票订单接口"""
    form_class = SubmitTicketOrderForm
    http_method_names = ['post']
    def form_invalid(self, form):
        err=json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err)
    def form_valid(self, form):
        obj =form.save(user=self.request.user)
        return http.JsonResponse({
            'sn' : obj.sn
        },status=201)

@method_decorator(login_required, name='dispatch')
class OrderDetail(BaseDetailView):
    slug_field = 'sn'
    slug_url_kwarg = 'sn'

    def get_queryset(self):
        user =self.request.user
        return Order.objects.filter(user=user, is_valid=True)

    def get(self,request, *args, **kwargs):
        """GET:订单详情"""
        order_obj = self.get_object()
        data = OrderDetailSerializer(order_obj).to_dict()
        return http.JsonResponse(data)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """POST订单支付"""
        # 选择支付方式 微信 支付宝
        # 数据验证
        order_obj=self.get_object()
        if order_obj.status==OrderStatus.SUBMIT:
            # 调用真实支付
            # 改变订单状态
            order_obj.status=OrderStatus.PAID
            order_obj.save()
            order_obj.order_items.update(status=OrderStatus.PAID)
            return http.HttpResponse('',status=201)
        return http.HttpResponse('',200)

    def delete(self, *args, **kwargs):
        """DELETE: 订单删除"""
        # 获取订单对象
        order_obj=self.get_object()
        # 验证数据（已支付、已取消）
        if order_obj.status==OrderStatus.CANCELED or order_obj.status==OrderStatus.PAID:
            if order_obj.is_valid:
                order_obj.is_valid=False
                order_obj.save()
                return http.HttpResponse('删除成功',status=201)
            else:
                # 此处不用写，因为get_object已经触发了404
                pass
        # 是否已经删除
        return http.HttpResponse('',200)
    @transaction.atomic
    def put(self, *args, **kwargs):
        """PUT：取消订单"""
        # 获取订单对象
        order_obj=self.get_object()
        # 数据验证
        if order_obj.status==OrderStatus.SUBMIT:
            # 改变状态
            order_obj.status=OrderStatus.CANCELED
            order_obj.save()
            items = order_obj.order_items.filter(status=OrderStatus.SUBMIT)
            # 加回已经扣减的库存
            for item in items:
                obj = item.content_object
                obj.remain_stock = F('remain_stock') + item.count
                obj.save()
            items.update(status=OrderStatus.CANCELED)

            return http.HttpResponse('1',status=201)

        return http.HttpResponse('2',status=200)


@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    """订单列表"""
    paginate_by = 10 #每页10条数据

    def get_queryset(self):
        user =self.request.user
        query = Q(is_valid=True,user=user)
        # 按状态查询
        status = self.request.GET.get('status',None)
        if status and status !='0':
            query =query & Q(status=status)
        return  Order.objects.filter(query)

    def render_to_response(self, context, **response_kwargs):
        """重写相应的返回"""
        page_obj = context['page_obj']
        if page_obj is not None:
            data=OrderListSeralizer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()

    def get_paginate_by(self, queryset):
        """根据接口参数limit控制分页大小"""
        page_size = self.request.GET.get('limit',None)
        return page_size or self.paginate_by