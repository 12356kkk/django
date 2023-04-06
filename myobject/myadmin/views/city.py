from django.http import JsonResponse
from django.shortcuts import render
from myadmin.models import city


def index(request):
    return render(request, "myadmin/index/index.html")

def showdata(request):
    list1 = []
    list2 = []
    ulist = city.objects.all()[:15]
    for ob in ulist:
        list1.append(ob.count)
        list2.append(ob.cityname)
        print(ob.cityname+' ')
    return JsonResponse({'data':list1,'city':list2})