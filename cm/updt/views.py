from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from car.models import Car
from updt.models import CarUpdate


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
    if VIN:
        cars = Car.objects.filter(VIN__contains=VIN)
    else:
        cars = Car.objects.all()
    data = []
    if cars.count() > int(limit):
        try:
            for i in range(int(limit) * (int(page) - 1), int(limit) * int(page)):
                if cars[i].status == 0:
                    data.append({
                        "id": i + 1,
                        "ICCID": cars[i].ICCID,
                        "VIN": cars[i].VIN,
                        "IP": cars[i].ip,
                        "version": cars[i].version,
                        'version_now': cars[i].version_now,
                        "status": '未升级',
                        'create_time': cars[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'status_code': cars[i].status_code
                    })
                if cars[i].status == 1:
                    data.append({
                        "id": i + 1,
                        "ICCID": cars[i].ICCID,
                        "VIN": cars[i].VIN,
                        "IP": cars[i].ip,
                        "version": cars[i].version,
                        'version_now': cars[i].version_now,
                        "status": '正在升级',
                        'create_time': cars[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'status_code': cars[i].status_code
                    })
                if cars[i].status == 2:
                    data.append({
                        "id": i + 1,
                        "ICCID": cars[i].ICCID,
                        "VIN": cars[i].VIN,
                        "IP": cars[i].ip,
                        "version": cars[i].version,
                        'version_now': cars[i].version_now,
                        "status": '升级完成',
                        'create_time': cars[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'status_code': cars[i].status_code
                    })
        except:
            data = []
            for i in range(int(limit) * (int(page) - 1), len(cars)):
                if cars[i].status == 0:
                    data.append({
                        "id": i+1,
                        "ICCID": cars[i].ICCID,
                        "VIN": cars[i].VIN,
                        "IP": cars[i].ip,
                        "version": cars[i].version,
                        'version_now': cars[i].version_now,
                        "status": '未升级',
                        'create_time': cars[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'status_code': cars[i].status_code
                    })
                if cars[i].status == 1:
                    data.append({
                        "id": i+1,
                        "ICCID": cars[i].ICCID,
                        "VIN": cars[i].VIN,
                        "IP": cars[i].ip,
                        "version": cars[i].version,
                        'version_now': cars[i].version_now,
                        "status": '正在升级',
                        'create_time': cars[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'status_code': cars[i].status_code
                    })
                if cars[i].status == 2:
                    data.append({
                        "id": i+1,
                        "ICCID": cars[i].ICCID,
                        "VIN": cars[i].VIN,
                        "IP": cars[i].ip,
                        "version": cars[i].version,
                        'version_now': cars[i].version_now,
                        "status": '升级完成',
                        'create_time': cars[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'status_code': cars[i].status_code
                    })
    else:
        for i in range(len(cars)):
            if cars[i].status == 0:
                data.append({
                    "id": i + 1,
                    "ICCID": cars[i].ICCID,
                    "VIN": cars[i].VIN,
                    "IP": cars[i].ip,
                    "version": cars[i].version,
                    'version_now':cars[i].version_now,
                    "status":  '未升级',
                    'create_time': cars[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'status_code': cars[i].status_code
                })
            if cars[i].status == 1:
                data.append({
                    "id": cars[i].id,
                    "ICCID": cars[i].ICCID,
                    "VIN": cars[i].VIN,
                    "IP": cars[i].ip,
                    "version": cars[i].version,
                    'version_now': cars[i].version_now,
                    "status":  '正在升级',
                    'create_time': cars[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'status_code': cars[i].status_code
                })
            if cars[i].status == 2:
                data.append({
                    "id": cars[i].id,
                    "ICCID": cars[i].ICCID,
                    "VIN": cars[i].VIN,
                    "IP": cars[i].ip,
                    "version": cars[i].version,
                    'version_now': cars[i].version_now,
                    "status": '升级完成',
                    'create_time': cars[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'status_code': cars[i].status_code
                })
    result = {"code": 0, "msg": "成功", "count": cars.count(), "data": data}
    return JsonResponse(result)
