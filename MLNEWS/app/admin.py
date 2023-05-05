from django.contrib import admin
from app.models import *
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # list_display用于设置列表页面要显示的不同字段
    list_display = ['id','name','tel','password']
    # search_fields用于设置搜索栏中要搜索的不同字段
    search_fields = ['id','name','tel','password']



@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    # list_display用于设置列表页面要显示的不同字段
    list_display = ['id','code','name','date','open','high','close','low','volume']
    # search_fields用于设置搜索栏中要搜索的不同字段
    search_fields =['id','code','name','date','open','high','close','low','volume']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # list_display用于设置列表页面要显示的不同字段
    list_display = ['id','title','date','src','today']
    # search_fields用于设置搜索栏中要搜索的不同字段
    search_fields =['id','title','date','src','today']

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    # list_display用于设置列表页面要显示的不同字段
    list_display = ['id','code','user']
    # search_fields用于设置搜索栏中要搜索的不同字段
    search_fields =['id','code','user']

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    # list_display用于设置列表页面要显示的不同字段
    list_display = ['id','code','user','time']
    # search_fields用于设置搜索栏中要搜索的不同字段
    search_fields =['id','code','user','time']
