import os
import time
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket
from django_redis import get_redis_connection
# Create your views here.

from car.excle import ExcelImport
from car.form import FileForm
from car.models import Car, CaseFile


def manage(request):
    VIN = request.GET.get('key[VIN]')
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if not page or not limit:
        page = 1
        limit = 10
    if VIN:
        cars = Car.objects.filter(VIN__contains=VIN).all()
    else:
        cars = Car.objects.all()
    data = []
    need_cans = cars[int(limit) * (int(page) - 1): int(limit) * int(page)]
    for i in range(len(need_cans)):
        data.append({
            "id": i + 1,
            "VIN": need_cans[i].VIN,
            "car_num": need_cans[i].car_num,
            "ICCID": need_cans[i].ICCID,
            "driver": need_cans[i].driver,
            'dept': need_cans[i].dept,
            'create_time': need_cans[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
        })
    result = {"code": 0, "msg": "成功", "count": cars.count(), "data": data}
    return JsonResponse(result)


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


def car_edit(request):
    """
    修改信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        VIN = request.GET.get('VIN')
        car = Car.objects.filter(VIN=VIN).first()
        content = {'car': car}
        return render(request, 'car_edit.html', content)
    if request.method == 'POST':
        VIN = request.POST.get('VIN')
        car_num = request.POST.get('car_num')
        ICCID = request.POST.get('ICCID')
        driver = request.POST.get('driver')
        dept = request.POST.get('dept')
        car = Car.objects.filter(VIN=VIN).first()
        car.car_num = car_num
        car.ICCID = ICCID
        car.driver = driver
        car.dept = dept
        car.save()
        return HttpResponse('<div style="color: #0dc316; text-align: center; margin-top: 100px; font-size: 50px">添加成功！!!</div>')


def car_del(request):
    """
    删除车辆信息
    :param request:
    :param id:
    :return:
    """
    VIN = request.GET.get('VIN')
    Car.objects.filter(VIN=VIN).delete()
    result = {'opt': '操作成功'}
    return JsonResponse(result)


def car_search(request):
    """
    查询车辆信息
    :param request:
    :return:
    """
    return render(request, 'car_list.html')


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
    pwd = os.path.dirname(os.path.dirname(__file__))
    file = open(pwd + '/static/excel_models/car_model.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="car_model.xls"'
    return response


def car_index(request):
    if request.method == 'GET':
        return render(request, 'car_monitor.html')


@accept_websocket
def car_monitor(request):
    if request.is_websocket():
        VIN = request.websocket.wait()  # 接受前段发送来的数据
        r = get_redis_connection('default')
        car_online = r.zrange('car_login', 0, -1)
        if VIN not in car_online:
            request.websocket.send('设备未登录,请连接设备'.encode())
            request.websocket.close()
        else:
            car = Car.objects.filter(VIN=VIN.decode('utf-8')).first()
            while True:
                can = car.can_set.all().order_by('-ter_time').first()
                request.websocket.send(can.data.encode())  # 发送给前段的数据
                time.sleep(10)
