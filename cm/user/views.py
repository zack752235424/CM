import hashlib

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import render


from user.form import UserForm, UserFormAdd, UserFormEdit
from user.models import User, Role


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
    users = User.objects.filter(is_delete=0).all()
    return render(request, 'member_list.html', {'users': users})


def member_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'member_add.html')
    if request.method == 'POST':
        form = UserFormAdd(request.POST)
        if form.is_valid():
            m = hashlib.md5(form.cleaned_data['passd'].encode())
            User.objects.create(username=form.cleaned_data['username'], pwd=m.hexdigest())
            user = User.objects.filter(username=form.cleaned_data['username']).first()
            if form.cleaned_data.get('read'):
                role = Role.objects.filter(rolename='管理员').first()
                user.roles.add(role)
            if form.cleaned_data.get('write'):
                role = Role.objects.filter(rolename='超级管理员').first()
                user.roles.add(role)
            return HttpResponse('<div style="color: #0dc316; text-align: center; margin-top: 100px; font-size: 50px">添加成功！!!</div>')
        errors = form.errors
        return render(request, 'member_add.html', {'errors':errors})


def edit(request, id):
    if request.method == 'GET':
        user = User.objects.get(pk=id)
        return render(request, 'member_edit.html', {'user': user})
    if request.method == 'POST':
        form = UserFormEdit(request.POST)
        user = User.objects.get(pk=id)
        if form.is_valid():
            m = hashlib.md5(form.cleaned_data['passd'].encode())
            user.pwd = m.hexdigest()
            if form.cleaned_data.get('read'):
                user.roles.set([2])
            if form.cleaned_data.get('write'):
                user.roles.set([1])
            user.save()
            return HttpResponse('<div style="color: #0dc316; text-align: center; margin-top: 100px; font-size: 50px">修改成功！!!</div>')
        errors = form.errors
        return render(request, 'member_edit.html', {'errors': errors, 'user': user})


def member_del(request):
    id = request.GET.get('id')
    User.objects.get(pk=id).delete()
    result = {'opt': '操作成功'}
    return JsonResponse(result)


def member_search(request):
    username = request.GET.get('username')
    users = User.objects.filter(username__contains=username).all()
    return render(request, 'member_list.html', {'users': users})
