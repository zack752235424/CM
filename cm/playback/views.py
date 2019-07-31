from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.
from playback.models import Back


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
    result = {'opts': [item for item in opts]}
    return JsonResponse(result)
