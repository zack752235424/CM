import os

import time
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render

# Create your views here.
from machine.excle import ExcelImport
from machine.form import FileForm
from machine.models import Machine, MachineFile


def index(request):
    return render(request, 'cps_machine.html')


def get_machine(request):
    ICCID = request.GET.get('key[ICCID]')
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    dept = request.GET.get('key[dept]')
    if ICCID or dept:
        machines = Machine.objects.filter(ICCID__contains=ICCID, dept__contains=dept).all()
    else:
        machines = Machine.objects.all()
    data = []
    need_cans = machines[int(limit) * (int(page) - 1): int(limit) * int(page)]
    for i in range(len(need_cans)):
        data.append({
            "id": i + 1,
            "ICCID": need_cans[i].ICCID,
            "product_num": need_cans[i].product_num,
            "serial_num": need_cans[i].serial_num,
            'birthday': need_cans[i].birthday,
            'create_time': need_cans[i].create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'dept': need_cans[i].dept,
        })
    result = {"code": 0, "msg": "成功", "count": machines.count(), "data": data}
    return JsonResponse(result)


def machine_edit(request):
    if request.method == 'GET':
        ICCID = request.GET.get('ICCID')
        machine = Machine.objects.filter(ICCID=ICCID).first()
        return render(request, 'machine_edit.html', {'machine': machine})
    if request.method == 'POST':
        ICCID = request.POST.get('ICCID')
        product_num = request.POST.get('product_num')
        serial_num = request.POST.get('serial_num')
        birthday = request.POST.get('birthday')
        dept = request.POST.get('dept')
        try:
            machine = Machine.objects.filter(ICCID=ICCID).first()
            machine.product_num = product_num
            machine.serial_num = serial_num
            machine.birthday = birthday
            machine.dept = dept
            machine.save()
            return HttpResponse('<div style="color: #0dc316; text-align: center; margin-top: 100px; font-size: 50px">添加成功！!!</div>')
        except:
            return HttpResponse('<div style="color: red; text-align: center; margin-top: 100px; font-size: 20px">编辑失败！！！</div>')


def machine_del(request):
    ICCID = request.GET.get('ICCID')
    Machine.objects.filter(ICCID=ICCID).delete()
    result = {'opt': '操作成功'}
    return JsonResponse(result)


def machine_add(request):
    if request.method == 'GET':
        return render(request, 'machine_add.html')
    if request.method == 'POST':
        ICCID = request.POST.get('ICCID')
        product_num = request.POST.get('product_num')
        serial_num = request.POST.get('serial_num')
        birthday = request.POST.get('birthday')
        dept = request.POST.get('dept')
        old_machines = Machine.objects.all()
        machines = [item.ICCID for item in old_machines]
        if ICCID not in machines:
            info = Machine.objects.create(ICCID=ICCID, product_num=product_num, serial_num=serial_num, birthday=birthday, dept=dept)
            info.save()
            return HttpResponse('<div style="color: #0dc316; text-align: center; margin-top: 100px; font-size: 50px">添加成功！!!</div>')
    return HttpResponse('<<div style="color: red; text-align: center; margin-top: 100px; font-size: 20px">请勿重复添加！！</div>')


def machine_download(request):
    pwd = os.path.dirname(os.path.dirname(__file__))
    file = open(pwd + '/static/excel_models/machine_model.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="machine_model.xls"'
    return response


def machine_upload(request):
    if request.method == 'GET':
        return render(request, 'machine_upload.html')
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = form.cleaned_data['files']
            name = time.time()
            file_name._set_name('%s.xls' % name)
            case_file = MachineFile.objects.create(file_name=file_name)
            case_file.save()
            messages = ExcelImport(file_name)
            messages.get_cases()
            Machine.objects.bulk_create(messages.cases)
            return HttpResponse('<div style="color: #0dc316; text-align: center; margin-top: 100px; font-size: 50px">上传成功！！！</div>')
        return HttpResponse('<div style="color: red; text-align: center; margin-top: 100px; font-size: 20px">上传错误,请上传xls文件！！！</div>')
