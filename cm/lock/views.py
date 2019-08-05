from django.shortcuts import render
from django_redis import get_redis_connection

# Create your views here.
r = get_redis_connection('default')


def lock(request):
    car_list = r.zrange('car', 0, -1)
    result = {'car_list': car_list}
    return render(request, 'lock.html', result)


def llock(request):
    VIN = request.GET.get('VIN')
    r.zadd('car', )
    return render(request, 'lock.html')


def unlock(request):
    return render(request, 'lock.html')
