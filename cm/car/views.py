import time
import xlwt
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from car.excle import ExcelImport
from car.form import FileForm
from car.models import Car, CaseFile


def manage(request):
    car_list = Car.objects.all()
    content = {'car_list': car_list, 'info': '请输入位VIN码或车牌号', 'len': len(car_list)}
    return render(request, 'car_list.html', content)


def car_add(request):
    """
    添加车辆
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'car_add.html')
    if request.method == 'POST':
        VIN = request.POST.get('VIN')
        car_num = request.POST.get('num')
        ICCID = request.POST.get('ICCID')
        driver = request.POST.get('driver')
        dept = request.POST.get('dept')
        old_cars = Car.objects.all()
        cars = [item.VIN for item in old_cars]
        if VIN not in cars:
            info = Car.objects.create(VIN=VIN, car_num=car_num, ICCID=ICCID, driver=driver, dept=dept)
            info.save()
            return HttpResponse('<div style="color: #0dc316; text-align: center; margin-top: 100px; font-size: 50px">添加成功！!!</div>')
    return HttpResponse('<<div style="color: red; text-align: center; margin-top: 100px; font-size: 20px">请勿重复添加！！</div>')


def car_edit(request, id):
    """
    修改信息
    :param request:
    :param id:
    :return:
    """
    if request.method == 'GET':
        car = Car.objects.get(pk=id)
        content = {'car': car}
        return render(request, 'car_edit.html', content)
    if request.method == 'POST':
        VIN = request.POST.get('VIN')
        car_num = request.POST.get('car_num')
        ICCID = request.POST.get('ICCID')
        driver = request.POST.get('driver')
        dept = request.POST.get('dept')
        car = Car.objects.get(pk=id)
        car.VIN = VIN
        car.car_num = car_num
        car.ICCID = ICCID
        car.driver = driver
        car.dept = dept
        car.save()
        return HttpResponse('<div style="color: #0dc316; text-align: center; margin-top: 100px; font-size: 50px">添加成功！!!</div>')


def car_del(request, id):
    """
    删除车辆信息
    :param request:
    :param id:
    :return:
    """
    Car.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('car:manage'))


def car_search(request):
    """
    查询车辆信息
    :param request:
    :return:
    """
    search = request.GET.get('search')
    if len(search) == 17:
        car_list = Car.objects.filter(VIN=search).all()
        if not car_list:
            info = '无此车辆信息,请重新输入'
            return render(request, 'car_list.html', {'info': info, 'len': 0})
        info = '查询成功'
        content = {'car_list': car_list, 'info': info, 'len': len(car_list)}
        return render(request, 'car_list.html', content)

    car_list = Car.objects.filter(car_num=search).all()
    if not car_list:
        info = '无此车辆信息,请重新输入'
        return render(request, 'car_list.html', {'info': info, 'len': 0})
    info = '查询成功'
    content = {'car_list': car_list, 'info': info, 'len': len(car_list)}
    return render(request, 'car_list.html', content)


def car_upload(request):
    """
    上传车辆信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'car_upload.html')
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = form.cleaned_data['files']
            name = time.time()
            file_name._set_name('%s.xls'%name)
            case_file = CaseFile.objects.create(file_name=file_name)
            case_file.save()
            messages = ExcelImport(file_name)
            messages.get_cases()
            Car.objects.bulk_create(messages.cases)
            return HttpResponse('<div style="color: #0dc316; text-align: center; margin-top: 100px; font-size: 50px">上传成功！！！</div>')
        return HttpResponse('<div style="color: red; text-align: center; margin-top: 100px; font-size: 20px">上传错误,请上传xls文件！！！</div>')


def car_download(request):
    """
    下载基础模板
    :param request:
    :return:
    """
    file = open('static/excel_models/car_model.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="car_model.xls"'
    return response
