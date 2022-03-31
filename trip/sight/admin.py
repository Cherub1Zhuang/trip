import json

from django.contrib import admin

# Register your models here.
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage

from sight import serializers
from sight.models import Sight, Info, Comment, Ticket
from utils import constants
from utils.actions import set_valid, set_invalid


@admin.register(Sight)
class SightAdmin(admin.ModelAdmin):
    """景点基础信息"""
    list_display = ('name','desc','main_img','score','province','city','area','town','is_valid','created_at','updated_at')
    search_fields = ('name','desc')
    list_filter = ('is_top','is_hot')
    list_per_page = 20
    actions = [set_invalid,set_valid]

    def cache_top_sight(self):
        """缓存精选景点"""
        queryset=Sight.objects.filter(is_valid=True,is_top=True)
        try:
            p=Paginator(queryset,20)
            page_obj=p.page(1)
            data = serializers.SightListSerializer(page_obj).to_dict()
            cache.set(constants.INDEX_SIGHT_TOP_KEY,json.dumps(data), constants.INDEX_SIGHT_TIMEOUT)
        except EmptyPage as e:
            print('暂无数据',e)
        except Exception as e:
            print('缓存失败',e)
    def cache_hot_sight(self):
        """缓存热门景点"""
        queryset=Sight.objects.filter(is_valid=True,is_hot=True)
        try:
            p=Paginator(queryset,20)
            page_obj=p.page(1)
            data = serializers.SightListSerializer(page_obj).to_dict()
            cache.set(constants.INDEX_SIGHT_HOT_KEY,json.dumps(data), constants.INDEX_SIGHT_TIMEOUT)
        except EmptyPage as e:
            print('暂无数据',e)
        except Exception as e:
            print('缓存失败',e)

    def save_form(self, request, form, change):
        """新增、修改的时候缓存数据"""
        obj=super().save_form(request, form, change)
        # 将热门、精选景点缓存到数据库
        self.cache_top_sight()
        self.cache_hot_sight()
        return obj
    def delete_model(self, request, obj):
        """物理删除的时候更新redis缓存"""
        # 将热门、精选景点缓存到数据库
        self.cache_top_sight()
        self.cache_hot_sight()
        return super().delete_model(request,obj)

@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    """景点详情"""
    list_display = ('sight','entry_explain','play_way','tips','traffic')
    search_fields = ('sight__name',)

@admin.register(Comment)
class InfoAdmin(admin.ModelAdmin):
    """景点详情"""
    list_display = ('user','sight','content','score','is_top','love_count')
    search_fields = ('sight__name',)
    actions = [set_invalid,set_valid]

@admin.register(Ticket)
class InfoAdmin(admin.ModelAdmin):
    """景点详情"""
    list_display = ('sight','name','types','price','discount','total_stock','remain_stock','is_valid')
    search_fields = ('sight__name',)
    actions = [set_invalid,set_valid]
