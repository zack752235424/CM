from django.shortcuts import render
from django_redis import get_redis_connection
from django.http import HttpResponseRedirect
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
    return render(request, 'lock.html', result)


def llock(request, VIN):
    r.zadd('car', {VIN: 1})
    return HttpResponseRedirect(reverse('lock:lock'))


def unlock(request, VIN):
    r.zadd('car', {VIN: 2})
    return HttpResponseRedirect(reverse('lock:lock'))


def search(request):
    VIN = request.GET.get('search')
    car_lis = []
    num = r.zscore('car', VIN)
    if not num:
        return HttpResponseRedirect(reverse('lock:lock'))
    score_o = int(num)
    score_c = r.zscore('car_status', VIN)
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
    car_lis.append((VIN, status, check))
    result = {'car_lis': car_lis}
    return render(request, 'lock.html', result)


def check_status(request, VIN):
    """
    车辆状态查询
    :param request:
    :param VIN:
    :return:
    """
    r.zadd('car_status', {VIN: 3})
    return HttpResponseRedirect(reverse('lock:lock'))
