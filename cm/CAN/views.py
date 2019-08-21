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
        cans = car.can_set.all().order_by('-ter_time')
    else:
        cans = car.can_set.all().filter(create_time__range=(stime, etime)).order_by('-ter_time')
    data = []
    for i in range(int(limit) * (int(page) - 1), int(limit) * int(page)):
        if cans[i].type == 1:
            data.append({
                "id": i+1,
                "VIN": VIN,
                'create_time': cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": cans[i].data,
                "type": '车辆登入报文',
            })
        elif cans[i].type == 2:
            data.append({
                "id": i+1,
                "VIN": VIN,
                'create_time': cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": cans[i].data,
                "type": '实时信息报文',
            })
        elif cans[i].type == 3:
            data.append({
                "id": i+1,
                "VIN": VIN,
                'create_time': cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": cans[i].data,
                "type": '补发信息报文',
            })
        elif cans[i].type == 4:
            data.append({
                "id": i+1,
                "VIN": VIN,
                'create_time': cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": cans[i].data,
                "type": '车辆登出报文',
            })
        elif cans[i].type == 80:
            data.append({
                "id": i+1,
                "VIN": VIN,
                'create_time': cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": cans[i].data,
                "type": '车辆升级报文',
            })
        elif cans[i].type == 1001:
            data.append({
                "id": i+1,
                "VIN": VIN,
                'create_time': cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": cans[i].data,
                "type": '信息上报错误',
            })
        elif cans[i].type == 1002:
            data.append({
                "id": i+1,
                "VIN": VIN,
                'create_time': cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": cans[i].data,
                "type": 'BCC校验失败',
            })
        elif cans[i].type == 1003:
            data.append({
                "id": i+1,
                "VIN": VIN,
                'create_time': cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": cans[i].data,
                "type": '车辆登录失败',
            })
    result = {"code": 0, "msg": "成功", "count": cans.count(), "data": data}
    return JsonResponse(result)

