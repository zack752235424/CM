from django.shortcuts import render
from django_redis import get_redis_connection
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

# Create your views here.
from car.models import Car

r = get_redis_connection('default')


def lock(request):
    cars = Car.objects.all()
    car_list = r.zrange('car', 0, -1)
    car_lists = r.zrange('car_status', 0, -1)
    for car in cars:
        if car.VIN.encode('utf-8') not in car_list:
            r.zadd('car', {car.VIN: 10})
    for car in cars:
        if car.VIN.encode('utf-8') not in car_lists:
            r.zadd('car_status', {car.VIN: 10})
    VIN = request.GET.get('key[VIN]')
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if not page or not limit:
        page = 1
        limit = 10
    if VIN:
        cars = Car.objects.filter(VIN__contains=VIN).all()
    else:
        cars = Car.objects.all()
    data = []
    need_cans = cars[int(limit) * (int(page) - 1): int(limit) * int(page)]
    for i in range(len(need_cans)):
        score_o = int(r.zscore('car', need_cans[i].VIN))
        score_c = int(r.zscore('car_status', need_cans[i].VIN))
        data.append({
            "id": i + 1,
            "VIN": need_cans[i].VIN,
            "status": '锁车中' if(score_o == 1) else ('解锁中' if(score_o == 2) else ('操作成功' if(score_o == 3) else '')),
            "check": '车辆已锁车' if(score_c == 1) else('车辆已解锁' if(score_c == 2) else ('车辆查询中' if(score_c == 3) else '')),
        })
    result = {"code": 0, "msg": "成功", "count": cars.count(), "data": data}
    return JsonResponse(result)


def llock(request):
    VIN = request.GET.get('VIN')
    r.zadd('car', {VIN: 1})
    return HttpResponseRedirect(reverse('lock:lock'))


def unlock(request):
    VIN = request.GET.get('VIN')
    r.zadd('car', {VIN: 2})
    return HttpResponseRedirect(reverse('lock:lock'))


def search(request):
    return render(request, 'lock.html')


def check_status(request):
    """
    车辆状态查询
    :param request:
    :param VIN:
    :return:
    """
    VIN = request.GET.get('VIN')
    r.zadd('car_status', {VIN: 3})
    return HttpResponseRedirect(reverse('lock:lock'))


def ledao_lock(request):
    cars = Car.objects.filter(dept='乐道汽车').all()
    car_list = r.zrange('car', 0, -1)
    car_lists = r.zrange('car_status', 0, -1)
    for car in cars:
        if car.VIN.encode('utf-8') not in car_list:
            r.zadd('car', {car.VIN: 10})
    for car in cars:
        if car.VIN.encode('utf-8') not in car_lists:
            r.zadd('car_status', {car.VIN: 10})
    car_lis = []
    for item in cars:
        score_o = int(r.zscore('car', item.VIN))
        score_c = int(r.zscore('car_status', item.VIN))
        if score_o == 1:
            status = '锁车中'
        elif score_o == 2:
            status = '解锁中'
        elif score_o == 3:
            status = '操作成功'
        else:
            status = ''
        if score_c == 1:
            check = '车辆已锁车'
        elif score_c == 2:
            check = '车辆已解锁'
        elif score_c == 3:
            check = '车辆查询中'
        else:
            check = ''
        car_lis.append((item.VIN, status, check))
    result = {'car_lis': car_lis}
    return render(request, 'ledao_lock.html',result)
