from django.http import JsonResponse
from django.shortcuts import render
from myadmin.models import salary


def index(request):
    return render(request, "myadmin/salary/index.html")

def showdata(request):
    list1 = []
    list2 = []
    ulist = salary.objects.all()[:21]
    for ob in ulist:
        list1.append(ob.count)
        list2.append(ob.salary)
        print(ob.salary+' ')
    return JsonResponse({'data':list1,'salary':list2})