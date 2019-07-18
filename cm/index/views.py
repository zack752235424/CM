import time

from django.http import JsonResponse
from django.shortcuts import render
from django_redis import get_redis_connection

# Create your views here.
from user.models import User


def index(request):
    rolename = User.objects.get(pk=1).roles.first().rolename
    return render(request, 'index.html', {'rolename': rolename})


def map(request):
    return render(request, 'baidu_map.html')


def get_data(request):
    result = {}
    return JsonResponse(result)
