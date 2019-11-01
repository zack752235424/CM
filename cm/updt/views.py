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
