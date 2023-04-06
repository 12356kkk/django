from django.http import JsonResponse
from django.shortcuts import render
from myadmin.models import job_name


def index(request):
    return render(request, "myadmin/job_name/index.html")

def showdata(request):
    list1 = []
    list2 = []
    ulist = job_name.objects.all()[:15]
    for ob in ulist:
        list1.append(ob.count)
        list2.append(ob.job_name)
        print(ob.job_name+' ')
    return JsonResponse({'data':list1,'job_name':list2})