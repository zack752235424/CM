from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


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
    return HttpResponseRedirect(reverse('playback:back_video'))
