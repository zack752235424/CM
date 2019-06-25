
import hashlib
from django.shortcuts import render

# Create your views here.
from user.models import User


def login(request):
    """
    登录页面
    :param request:username, password
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = User.objects.get()

