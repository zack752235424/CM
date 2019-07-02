from django.shortcuts import render

# Create your views here.
from user.models import User


def index(request):
    rolename = User.objects.get(pk=1).roles.first().rolename
    return render(request, 'index.html', {'rolename': rolename})


def map(request):
    return render(request, 'baidu_map.html')
