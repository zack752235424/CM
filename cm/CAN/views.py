import time
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from car.models import Car


def show(request):
    return render(request, 'can_list.html')


def can_search(request):
    VIN = request.GET.get('VIN')
    stime = request.GET.get('stime')
    etime = request.GET.get('etime')
    if not VIN:
        return HttpResponseRedirect(reverse('CAN:show'))
    car = Car.objects.filter(VIN=VIN).first()
    if not car:
        return HttpResponseRedirect(reverse('CAN:show'))
    if not stime or not etime:
        cans = car.can_set.all().order_by('-ter_time')
    else:
        cans = car.can_set.all().filter(create_time__range=(stime, etime)).order_by('-ter_time')
    pindex = request.GET.get("pindex")
    pageinator = Paginator(cans, 10)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    return render(request, 'can_list.html', {'page': page, 'VIN': VIN})


def analysis_data(request):
    data = request.GET.get('data')
    return render(request, 'analysis_data.html', {'data': data})


def test(request):
    s = time.time()
    VIN = request.GET.get('VIN')
    stime = request.GET.get('stime')
    etime = request.GET.get('etime')
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if not page or not limit:
        page = 1
        limit = 10
    if not VIN:
        return HttpResponseRedirect(reverse('CAN:show'))
    car = Car.objects.filter(VIN=VIN).first()
    if not car:
        return HttpResponseRedirect(reverse('CAN:show'))
    if not stime or not etime:
        cans = car.can_set.order_by('-ter_time').all()
    else:
        cans = car.can_set.filter(create_time__range=(stime, etime)).order_by('-ter_time').all()
    data = []
    need_cans = cans[int(limit) * (int(page) - 1): int(limit) * int(page)]
    for i in range(len(need_cans)):
        type = need_cans[i].type
        data.append({
            "id": int(limit) * (int(page) - 1) + i+1,
            "VIN": VIN,
            'create_time': need_cans[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": need_cans[i].data,
            "type": '车辆登入报文' if(type == 1) else ('实时信息报文' if(type == 2) else ('补发信息报文' if(type == 3) else('车辆登出报文' if(type == 4) else ('车辆升级报文' if(type == 80) else ('信息上报错误' if(type == 1001) else ('BCC校验失败' if(type == 1002) else ('车辆登录失败' if(type == 1003) else '自定义信息'))))))),
        })
    result = {"code": 0, "msg": "成功", "count": cans.count(), "data": data}
    print(time.time() - s, '总计花费时间')
    return JsonResponse(result)

