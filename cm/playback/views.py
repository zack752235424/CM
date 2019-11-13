from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
# Create your views here.
from car.models import Car
from playback.models import Back
from django_redis import get_redis_connection


def back_video(request):
    """
    轨迹回放页
    :param request:
    :return:
    """
    return render(request, 'back_video.html')


def search(request):
    """
    轨迹回放查询
    :param request:
    :return:
    """
    VIN = request.GET.get('VIN')
    stime = request.GET.get('stime')
    etime = request.GET.get('etime')
    opts = Back.objects.values_list('longitude', 'latitude').filter(Q(VIN=VIN) & Q(create_time__range=(stime, etime))).all()
    if opts:
        result = {'opts': [item for item in opts]}
    else:
        result = {'opts': 'failure'}
    return JsonResponse(result)


def data_recovery(request):
    cars = Car.objects.all()
    r = get_redis_connection('default')
    for car in cars:
        back = Back.objects.filter(VIN=car.VIN).order_by('-id').first()
        if back:
            r.geoadd('car_offline', back.longitude, back.latitude, back.VIN)
    return HttpResponse('<div style="color: red; text-align: center; margin-top: 100px; font-size: 20px">数据恢复成功</div>')

