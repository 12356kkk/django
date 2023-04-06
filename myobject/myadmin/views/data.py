# 会员信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
# Create your views here.
from myadmin.models import Data


def index(request, pIndex=1):
    '''浏览信息'''
    umod = Data.objects

    ulist = umod.order_by("id")  # 对id排序
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 10)  # 以每页5条数据分页
    maxpages = page.num_pages  # 获取最大页数
    # 判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {"datalist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages}
    return render(request, "myadmin/data/index.html", context)