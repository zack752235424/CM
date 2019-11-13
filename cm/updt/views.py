import xlwt
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from car.models import Car
from updt.models import CarUpdate
from django.http import FileResponse



def up(request):
    if request.method == 'GET':
        return render(request, 'up.html')
    if request.method == 'POST':
        ICCID = request.POST.get('ICCID')
        VIN = request.POST.get('VIN')
        version = request.POST.get('version')
        ip = request.POST.get('ip')
        ftp = request.POST.get('ftp')
        pwd = request.POST.get('pwd')
        CarUpdate.objects.create(ICCID=ICCID, VIN=VIN, version=version, ip=ip, ftp=ftp, pwd=pwd)
        if ICCID:
            if len(ICCID) == 20:
                car = Car.objects.filter(ICCID=ICCID).first()
                car.version = version
                car.ip = ip
                car.ftp = ftp
                car.pwd = pwd
                car.status = 0
                car.save()
            else:
                ICCIDS = ICCID.split(',')
                for item in ICCIDS:
                    car = Car.objects.filter(ICCID=item).first()
                    car.version = version
                    car.ip = ip
                    car.ftp = ftp
                    car.pwd = pwd
                    car.status = 0
                    car.save()
        if VIN:
            if len(VIN) == 17:
                car = Car.objects.filter(VIN=VIN).first()
                car.version = version
                car.ip = ip
                car.ftp = ftp
                car.pwd = pwd
                car.status = 0
                car.save()
            else:
                VINS = VIN.split(',')
                for item in VINS:
                    car = Car.objects.filter(VIN=item).first()
                    car.version = version
                    car.ip = ip
                    car.ftp = ftp
                    car.pwd = pwd
                    car.status = 0
                    car.save()
        return render(request, 'up.html')


def get_users(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    VIN = request.GET.get('key[id]')
    dept = request.GET.get('key[dept]')
    if VIN or dept:
        cars = Car.objects.filter(VIN__contains=VIN, dept__contains=dept)
    else:
        cars = Car.objects.all()
    data = []
    need_cans = cars[int(limit) * (int(page) - 1): int(limit) * int(page)]
    for i in range(len(need_cans)):
        type = need_cans[i].status
        data.append({
            "id": i + 1,
            "ICCID": need_cans[i].ICCID,
            "VIN": need_cans[i].VIN,
            "IP": need_cans[i].ip,
            "version": need_cans[i].version,
            'version_now': need_cans[i].version_now,
            "status": '未升级' if(type == 0) else ('正在升级' if (type == 1) else ('升级完成' if(type == 2) else '')),
            'create_time': need_cans[i].create_time.strftime("%Y-%m-%d %H:%M:%S") if (need_cans[i].create_time) else '',
            'status_code': need_cans[i].status_code
        })
    result = {"code": 0, "msg": "成功", "count": cars.count(), "data": data}
    return JsonResponse(result)


def up_download(request):
    cars = Car.objects.all()
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('车辆升级信息')
    # 写入excel
    # 参数对应 行, 列, 值
    worksheet.write(0, 0, label='VIN码')
    worksheet.write(0, 1, label='ICCID')
    worksheet.write(0, 2, label='时间')
    worksheet.write(0, 3, label='当前版本号')
    worksheet.write(0, 4, label='升级版本号')
    worksheet.write(0, 5, label='状态')
    worksheet.write(0, 6, label='状态码')
    worksheet.write(0, 7, label='部门')
    for i in range(len(cars)):
        type = cars[i].status
        worksheet.write(i + 1, 0, label=(cars[i].VIN))
        worksheet.write(i + 1, 1, label=(cars[i].ICCID))
        worksheet.write(i + 1, 2, label=(cars[i].create_time.strftime("%Y-%m-%d %H:%M:%S") if (cars[i].create_time) else ''))
        worksheet.write(i + 1, 3, label=(cars[i].version_now))
        worksheet.write(i + 1, 4, label=(cars[i].version))
        worksheet.write(i + 1, 5, label=('未升级' if(type == 0) else ('正在升级' if (type == 1) else ('升级完成' if(type == 2) else ''))))
        worksheet.write(i + 1, 6, label=(cars[i].status_code))
        worksheet.write(i + 1, 7, label=(cars[i].dept))
    # 保存
    worksheet.col(0).width = 256 * 20
    worksheet.col(1).width = 256 * 25
    worksheet.col(2).width = 256 * 18
    worksheet.col(3).width = 256 * 18
    worksheet.col(4).width = 256 * 18
    worksheet.col(5).width = 256 * 18
    worksheet.col(6).width = 256 * 18
    workbook.save('./up_data.xls')
    file = open('./up_data.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="up_data.xls"'
    return response
