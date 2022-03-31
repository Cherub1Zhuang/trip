from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from accounts.forms import ProfileEditForm
from accounts.models import Profile, User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    """用户基础信息管理"""
    # 列表要显示的内容
    list_display = ('username','nickname','is_staff','is_active','date_joined')
    search_fields = ('username', 'nickname')
    # 新增表单
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,{'fields':('nickname',)}),
    )
    # 修改的表单
    fieldsets = UserAdmin.fieldsets + (
        (None,{'fields':('nickname','avatar')}),
    )

    actions = ['disable_user','enable_user']

    def disable_user(self,request,queryset):
        queryset.update(is_active=False)
    disable_user.short_description = '批量禁用用户'

    def enable_user(self,request,queryset):
        queryset.update(is_active=True)
    enable_user.short_description = '批量启用用户'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """用户详细信息表"""
    list_display = ('format_username', 'sex', 'age', 'created_at')
    # 每页显示数据
    list_per_page = 5
    # 关联字段一次查出，减少查询次数
    list_select_related = ('user',)
    # 快捷搜索
    list_filter = ('sex',)
    # 输入内容，模糊匹配
    search_fields = ('username','user__nickname')
    # 表单中可编辑的字段
    fields = ('real_name','email','phone_no','sex','age')
    # 自定义表单验证
    form=ProfileEditForm

    def format_username(self, obj):
        return obj.username[:3]+'***'
    format_username.short_description = '用户名'