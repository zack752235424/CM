

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render


from user.form import UserForm
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
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=form.cleaned_data['username'], pwd=form.cleaned_data['pwd']).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('index:index'))
        error = {[item for item in form.errors][0]: form.errors[[item for item in form.errors][0]]}
        return render(request, 'login.html', {'error': error})


def logout(request):
    """
    注销功能
    :param request:
    :return:
    """
    del request.session['user_id']
    return HttpResponseRedirect(reverse('user:login'))


def manage(request):
    """
    用户管理
    :param request:
    :return:
    """
    return render(request, 'member_list.html')


def member_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    return render(request, 'member_add.html')



