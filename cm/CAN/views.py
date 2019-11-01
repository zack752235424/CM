import time

import xlwt
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.http import FileResponse

# Create your views here.
from django.urls import reverse

from car.models import Car


def show(request):
    return render(request, 'can_list.html')


def can_search(request):
    VIN = request.GET.get('VIN')
    stime = request.GET.get('stime')
    etime = request.GET.get('etime')
    if not VIN:
        return HttpResponseRedirect(reverse('CAN:show'))
    car = Car.objects.filter(VIN=VIN).first()
    if not car:
        return HttpResponseRedirect(reverse('CAN:show'))
    if not stime or not etime:
        cans = car.can_set.all().order_by('-ter_time')
    else:
        cans = car.can_set.all().filter(create_time__range=(stime, etime)).order_by('-ter_time')
    pindex = request.GET.get("pindex")
    pageinator = Paginator(cans, 10)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    return render(request, 'can_list.html', {'page': page, 'VIN': VIN})


def analysis_data(request):
    data = request.GET.get('data')
    return render(request, 'analysis_data.html', {'data': data})


def test(request):
    VIN = request.GET.get('VIN')
    stime = request.GET.get('stime')
    etime = request.GET.get('etime')
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if not page or not limit:
        page = 1
        limit = 10
    if not VIN:
        return HttpResponseRedirect(reverse('CAN:show'))
    car = Car.objects.filter(VIN=VIN).first()
    if not car:
        return HttpResponseRedirect(reverse('CAN:show'))
    if not stime or not etime:
        cans = car.can_set.order_by('-ter_time').all()
    else:
        cans = car.can_set.filter(create_time__range=(stime, etime)).order_by('-ter_time').all()
    data = []
    need_cans = cans[int(limit) * (int(page) - 1): int(limit) * int(page)]
    for i in range(len(need_cans)):
        type = need_cans[i].type
        data.append({
            "id": int(limit) * (int(page) - 1) + i+1,
            "VIN": VIN,
            'create_time': need_cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": need_cans[i].data,
            "type": '车辆登入报文' if(type == 1) else ('实时信息报文' if(type == 2) else ('补发信息报文' if(type == 3) else('车辆登出报文' if(type == 4) else ('车辆升级报文' if(type == 80) else ('信息上报错误' if(type == 1001) else ('BCC校验失败' if(type == 1002) else ('车辆登录失败' if(type == 1003) else '自定义信息'))))))),
        })
    result = {"code": 0, "msg": "成功", "count": cans.count(), "data": data}
    return JsonResponse(result)


def can_download(request):
    if request.method == "GET":
        return render(request, 'can_download.html')
    if request.method == 'POST':
        VIN = request.POST.get('VIN')
        stime = request.POST.get('stime')
        etime = request.POST.get('etime')
        car = Car.objects.filter(~Q(dept='医疗') & Q(VIN=VIN)).first()
        if not car:
            result = {'error': 'VIN输入错误,请重新输入!', 'VIN': VIN, 'stime': stime, 'etime': etime}
            return render(request, 'doctor_download.html', result)
        cans = car.can_set.all().filter(Q(type=2 or 3) & Q(create_time__range=(stime, etime)))
        if not cans:
            result = {'error': '此时间段无数据,请重新输入!', 'VIN': VIN, 'stime': stime, 'etime': etime}
            return render(request, 'doctor_download.html', result)
        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        worksheet = workbook.add_sheet('整车数据信息')
        # 写入excel
        # 参数对应 行, 列, 值
        worksheet.write(0, 0, label='VIN码')
        worksheet.write(0, 1, label='报文时间')
        worksheet.write(0, 2, label='原始记录')
        worksheet.write(0, 3, label='车速')
        worksheet.write(0, 4, label='启动状态')
        worksheet.write(0, 5, label='运行模式')
        worksheet.write(0, 6, label='累计里程')
        worksheet.write(0, 7, label='档位')
        worksheet.write(0, 8, label='充电状态')
        worksheet.write(0, 9, label='最高电压电池子系统号')
        worksheet.write(0, 10, label='最高电压电池单体代号')
        worksheet.write(0, 11, label='电池单体电压最高值')
        worksheet.write(0, 12, label='最低电压电池子系统号')
        worksheet.write(0, 13, label='最低电压电池单体代号')
        worksheet.write(0, 14, label='电池单体电压最低值')
        worksheet.write(0, 15, label='最高温度子系统号')
        worksheet.write(0, 16, label='最高温度探针序号')
        worksheet.write(0, 17, label='最高温度值')
        worksheet.write(0, 18, label='最低温度子系统号')
        worksheet.write(0, 19, label='最低温度探针序号')
        worksheet.write(0, 20, label='最低温度值')
        worksheet.write(0, 21, label='加速踏板行程值')
        worksheet.write(0, 22, label='制动踏板状态')
        worksheet.write(0, 23, label='总电压')
        worksheet.write(0, 24, label='总电流')
        worksheet.write(0, 25, label='SOC')
        worksheet.write(0, 26, label='绝缘电阻')
        worksheet.write(0, 27, label='定位状态')
        worksheet.write(0, 28, label='经度')
        worksheet.write(0, 29, label='纬度')
        worksheet.write(0, 30, label='DC-DC状态')
        worksheet.write(0, 31, label='电机控制器直流母线电流')
        worksheet.write(0, 32, label='驱动电机个数')
        worksheet.write(0, 33, label='驱动电机序号')
        worksheet.write(0, 34, label='驱动电机状态')
        worksheet.write(0, 35, label='驱动电机控制器温度')
        worksheet.write(0, 36, label='驱动电机转速')
        worksheet.write(0, 37, label='驱动电机转矩')
        worksheet.write(0, 38, label='驱动电机温度')
        worksheet.write(0, 39, label='电机控制器输入电压')
        worksheet.write(0, 40, label='最高报警等级')
        worksheet.write(0, 41, label='通用报警标志')
        worksheet.write(0, 42, label='可充电储能装置故障总数')
        worksheet.write(0, 43, label='驱动电机故障总数')
        worksheet.write(0, 44, label='发动机故障总数')
        worksheet.write(0, 45, label='其他故障总数')
        worksheet.write(0, 46, label='可充电储能子系统个数-电压')
        worksheet.write(0, 47, label='可充电储能装置电压')
        worksheet.write(0, 48, label='可充电储能装置电流')
        worksheet.write(0, 49, label='单体电池总数')
        worksheet.write(0, 50, label='单体电池电压')
        worksheet.write(0, 51, label='可充电储能子系统个数-温度')
        worksheet.write(0, 52, label='可充电储能子系统号-温度')
        worksheet.write(0, 53, label='可充电储能温度探针个数')
        worksheet.write(0, 54, label='可充电储能装置温度数据')
        # worksheet.write(0, 55, label='燃料电池电压')
        # worksheet.write(0, 56, label='燃料电池电流')
        # worksheet.write(0, 57, label='燃料电池消耗率')
        # worksheet.write(0, 58, label='燃料电池温度探针总数')
        # worksheet.write(0, 59, label='氢气最高浓度')
        # worksheet.write(0, 60, label='氢气最高浓度传感器代号')
        # worksheet.write(0, 61, label='氢气最高压力')
        # worksheet.write(0, 62, label='氢气最高压力传感器代号')
        # worksheet.write(0, 63, label='氢系统中最高温度')
        # worksheet.write(0, 64, label='氢系统中最高温度代号')
        # worksheet.write(0, 65, label='探针温度值')
        # 232302fe54424f5843333241303030303030303035010109
        # 13091012020a
        # 050107397ea301df778d 定位信息数据
        # 3346060fbd271003b227222710000000840000005d000034d100003dcc03e8151f0a68000f09070000012701010000030000030902037d03b20b520b52037d0b55  医疗设备数据
        # 0801010000000000480001480fa30fa50fa70fab0fac0fa80fac0faa0faa0fab0fac0faa0fc60fc30fc20fc10fc60fc40fc40fbf0fc30fc10fc10fbb0fa80f
        # a80faa0fb00fb00fb40fb20fac0fae0fb20faf0fb20fd00fcb0fce0fc70fcd0fc90fc80fc80fc80fc60fc30fc00fbc0fc30fc10fc20fc60fc30fc50fc50fc40
        # fc60fc50fc40fce0fcb0fcc0fcc0fcc0fcd0fca0fcc0fca0fcb0fc60fc4  电压数据
        # 09010100084448464547462828  温度数据
        # 0601250fd001010fa3010248010728 b2 极值数据
        for i in range(len(cans)):
            message = cans[i].data
            data = message[60:-2]
            worksheet.write(i + 1, 0, label=VIN)
            worksheet.write(i + 1, 1, label=cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S"))
            worksheet.write(i + 1, 2, label=message)
            while data:
                if data[0:2] == '01':  # 整车数据
                    car = [data[i*2:(i+1)*2] for i in range(len(data)//2)]
                    if car[1] == '01':
                        worksheet.write(i + 1, 4, label='启动')  # 车辆状态
                    elif car[1] == '02':
                        worksheet.write(i + 1, 4, label='熄火')  # 车辆状态
                    elif car[1] == '03':
                        worksheet.write(i + 1, 4, label='其他')  # 车辆状态
                    elif int(car[1], 16) == 254:
                        worksheet.write(i + 1, 4, label='异常')  # 车辆状态
                    elif int(car[1], 16) == 255:
                        worksheet.write(i + 1, 4, label='无效')  # 车辆状态
                    else:
                        worksheet.write(i + 1, 4, label='错误')  # 车辆状态
                    if car[2] == '01':
                        worksheet.write(i + 1, 8, label='停车充电')  # 充电状态
                    elif car[2] == '02':
                        worksheet.write(i + 1, 8, label='行驶充电')  # 充电状态
                    elif car[2] == '03':
                        worksheet.write(i + 1, 8, label='未充电')  # 充电状态
                    elif car[2] == '04':
                        worksheet.write(i + 1, 8, label='充电完成')  # 充电状态
                    elif int(car[2], 16) == 254:
                        worksheet.write(i + 1, 8, label='异常')  # 充电状态
                    elif int(car[2], 16) == 255:
                        worksheet.write(i + 1, 8, label='无效')  # 充电状态
                    else:
                        worksheet.write(i + 1, 8, label='错误')  # 充电状态
                    if car[3] == '01':
                        worksheet.write(i + 1, 5, label='纯电')  # 运行模式
                    elif car[3] == '02':
                        worksheet.write(i + 1, 5, label='混动')  # 运行模式
                    elif car[3] == '03':
                        worksheet.write(i + 1, 5, label='燃油')  # 运行模式
                    elif int(car[3], 16) == 255:
                        worksheet.write(i + 1, 5, label='无效')  # 运行模式
                    else:
                        worksheet.write(i + 1, 5, label='错误')  # 运行模式
                    worksheet.write(i + 1, 3, label=str(((int(car[4], 16)*256)+int(car[5], 16))/10)+"km/h")  # 车速
                    worksheet.write(i + 1, 6, label=str(((int(car[6], 16)*256*256*256)+(int(car[7], 16)*256*256)+(int(car[8], 16)*256)+int(car[9], 16))/10) + "km")  # 累计里程
                    worksheet.write(i + 1, 23, label=str(((int(car[10], 16)*256)+int(car[11], 16))/10) + "V")  # 总电压
                    worksheet.write(i + 1, 24, label=str(((int(car[12], 16)*256)+int(car[13], 16)-10000)/10) + "A")  # 总电流
                    worksheet.write(i + 1, 25, label=str(int(car[14], 16))+" % --- 0x"+str(car[14]))  # SOC
                    if car[15] == '01':
                        worksheet.write(i + 1, 30, label='工作')  # DC-DC状态
                    worksheet.write(i + 1, 30, label='断开')  # DC-DC状态
                    d = car[16]
                    if int(d[1], 16) == 0:
                        worksheet.write(i + 1, 7, label='空挡')  # 档位
                    elif int(d[1], 16) == 13:
                        worksheet.write(i + 1, 7, label='倒挡')  # 档位
                    elif int(d[1], 16) == 14:
                        worksheet.write(i + 1, 7, label='自动D挡')  # 档位
                    elif int(d[1], 16) == 15:
                        worksheet.write(i + 1, 7, label='停车P挡')  # 档位
                    worksheet.write(i + 1, 26, label=str(int(car[17], 16)*256+int(car[18], 16))+"kΩ")  # 绝缘电阻
                    worksheet.write(i + 1, 21, label=str(int(car[19], 16)) + "%")  # 加速踏板行程值
                    worksheet.write(i + 1, 22, label=str(int(car[20], 16)) + "%")  # 制动踏板状态
                    data = data.replace(data[0:42], '', 1)
                if data[0:2] == '02':  # 驱动电机数据
                    motor = [data[i*2:(i+1)*2] for i in range(len(data)//2)]

                    worksheet.write(i + 1, 32, label=int(motor[1], 16))  # 驱动电机个数
                    worksheet.write(i + 1, 33, label=int(motor[2], 16))  # 驱动电机序号
                    if motor[3] == '01':
                        worksheet.write(i + 1, 34, label='耗电')  # 驱动电机状态
                    elif motor[3] == '02':
                        worksheet.write(i + 1, 34, label='发电')  # 驱动电机状态
                    elif motor[3] == '03':
                        worksheet.write(i + 1, 34, label='关闭')  # 驱动电机状态
                    elif motor[3] == '04':
                        worksheet.write(i + 1, 34, label='准备')  # 驱动电机状态
                    elif motor[3] == 'fe' or motor[3] == 'FE':
                        worksheet.write(i + 1, 34, label='异常')  # 驱动电机状态
                    elif motor[3]=='ff' or motor[3]=='FF':
                        worksheet.write(i + 1, 34, label='无效')  # 驱动电机状态
                    else:
                        worksheet.write(i + 1, 34, label='未知')  # 驱动电机状态
                    worksheet.write(i + 1, 35, label=str(int(motor[4], 16)-40) + "℃")  # 驱动电机控制器温度
                    worksheet.write(i + 1, 36, label=str((int(motor[5], 16)*256 + int(motor[6], 16))-20000) + "r/min")  # 驱动电机转速
                    worksheet.write(i + 1, 37, label=str((int(motor[7], 16)*256 + int(motor[8], 16))/10-2000) + "N·m")  # 驱动电机转矩
                    worksheet.write(i + 1, 38, label=str(int(motor[9], 16) - 40) + "℃")  # 驱动电机温度
                    worksheet.write(i + 1, 39, label=str((int(motor[10], 16)*256+int(motor[11], 16))/10) + "V")  # 电机控制器输入电压
                    worksheet.write(i + 1, 31, label=str((int(motor[12], 16)*256+int(motor[13], 16)-10000)/10) + "A")  # 电机控制器直流母线电流
                    len_m = 2 + int(data[2:4], 16) * 24
                    data = data.replace(data[0:2 + len_m], '', 1)
                if data[0:2] == '03':  # 燃料电池数据
                    data = data.replace(data[0:22], '', 1)
                if data[0:2] == '04':  # 发动机数据
                    data = data.replace(data[0:12], '', 1)
                if data[0:2] == '05':  # 车辆位置数据
                    if data[2:4] == '00':
                        longitude = int(data[4:12], 16) / 1000000
                        latitude = int(data[12:20], 16) / 1000000
                        worksheet.write(i + 1, 27, label='有效')  # 定位状态
                        worksheet.write(i + 1, 28, label=longitude)  # 经度
                        worksheet.write(i + 1, 29, label=latitude)  # 纬度
                    else:
                        worksheet.write(i + 1, 27, label='无效')  # 定位状态
                    data = data.replace(data[0:20], '', 1)
                if data[0:2] == '06':  # 极值数据
                    # 0601250fd001010fa3010248010728  极值数据
                    limit = [data[i*2:(i+1)*2] for i in range(len(data)//2)]
                    worksheet.write(i + 1, 9, label=int(limit[1], 16))  # 最高电压电池子系统号
                    worksheet.write(i + 1, 10, label=int(limit[2], 16))  # 最高电压电池单体代号
                    worksheet.write(i + 1, 11, label=str((int(limit[3], 16)*256+int(limit[4], 16))/1000) + "V")  # 电池单体电压最高值
                    worksheet.write(i + 1, 12, label=int(limit[5], 16))  # 最低电压电池子系统号
                    worksheet.write(i + 1, 13, label=int(limit[6], 16))  # 最低电压电池单体代号
                    worksheet.write(i + 1, 14, label=str((int(limit[7], 16)*256+int(limit[8], 16))/1000) + "V")  # 电池单体电压最低值
                    worksheet.write(i + 1, 15, label=int(limit[9], 16))  # 最高温度子系统号
                    worksheet.write(i + 1, 16, label=int(limit[10], 16))  # 最高温度探针序号
                    worksheet.write(i + 1, 17, label=str(int(limit[11], 16)-40)+"℃")  # 最高温度值
                    worksheet.write(i + 1, 18, label=int(limit[12], 16))  # 最低温度子系统号
                    worksheet.write(i + 1, 19, label=int(limit[13], 16))  # 最低温度探针序号
                    worksheet.write(i + 1, 20, label=str(int(limit[14], 16)-40) + "℃")  # 最低温度值
                    data = data.replace(data[0:30], '', 1)
                if data[0:2] == '07':  # 报警数据
                    worksheet.write(i + 1, 40, label=int(data[2:4], 16))  # 最高报警等级
                    worksheet.write(i + 1, 41, label=data[4:12])  # 通用报警标志
                    data = data.replace(data[0:12], '', 1)
                    num1 = data[0:2]
                    worksheet.write(i + 1, 42, label=int(num1, 16))  # 可充电储能装置故障总数
                    if num1 != '00':
                        len1 = int(num1, 16) * 8
                        data = data.replace(data[0:2 + len1], '', 1)
                    else:
                        data = data.replace(data[0:2], '', 1)
                    num2 = data[0:2]
                    worksheet.write(i + 1, 43, label=int(num2, 16))  # 驱动电机故障总数
                    if num2 != '00':
                        len2 = int(num1, 16) * 8
                        data = data.replace(data[0:2 + len2], '', 1)
                    else:
                        data = data.replace(data[0:2], '', 1)
                    num3 = data[0:2]
                    worksheet.write(i + 1, 44, label=int(num3, 16))  # 发动机故障总数
                    if num3 != '00':
                        len3 = int(num1, 16) * 8
                        data = data.replace(data[0:2 + len3], '', 1)
                    else:
                        data = data.replace(data[0:2], '', 1)
                    num4 = data[0:2]
                    worksheet.write(i + 1, 45, label=int(num4, 16))  # 其他故障总数
                    if num4 != '00':
                        len4 = int(num1, 16) * 8
                        data = data.replace(data[0:2 + len4], '', 1)
                    else:
                        data = data.replace(data[0:2], '', 1)
                if data[0:2] == '08':  # 电池电压数据
                    num = int(data[2:4], 16)
                    worksheet.write(i + 1, 46, label=int(str(num), 16))  # 可充电储能子系统个数-电压
                    while num != 0:
                        worksheet.write(i + 1, 47, label=int(data[6: 10], 16))  # 可充电储能装置电压
                        worksheet.write(i + 1, 48, label=int(data[10: 14], 16))  # 可充电储能装置电流
                        num_battery = int(data[22:24], 16)
                        worksheet.write(i + 1, 49, label=num_battery)  # 单体电池总数
                        total_V = ''
                        for b in range(0, num_battery):
                            v = str(int(data[24 + 4 * b: 24 + 4 * (b + 1)], 16)/1000)
                            if b != num_battery - 1:
                                total_V += v + ','
                            else:
                                total_V += v
                        worksheet.write(i + 1, 50, label=total_V)  # 单体电池电压
                        total_len = num_battery * 4
                        data = data.replace(data[4: 4 + 20 + total_len], '', 1)
                        num -= 1
                    data = data.replace(data[0:4], '', 1)
                if data[0:2] == '09':  # 电池温度数据
                    num = int(data[2:4], 16)
                    worksheet.write(i + 1, 51, label=int(str(num), 16))  # 可充电储能子系统个数-温度
                    while num != 0:
                        worksheet.write(i + 1, 52, label=int(data[4: 6], 16))  # 可充电储能子系统号-温度
                        num_temp = int(data[6:10], 16)
                        worksheet.write(i + 1, 53, label=num_temp)  # 可充电储能温度探针个数
                        total_C = ''
                        for c in range(0, num_temp):
                            C = str(int(data[10 + 2*c: 10 + 2 * (c+1)], 16) - 40)
                            if c != num_temp -1:
                                total_C += C + ','
                            else:
                                total_C += C
                        worksheet.write(i + 1, 54, label=total_C)  # 可充电储能装置温度数据
                        total_len = num_temp * 2
                        data = data.replace(data[4:4 + 6 + total_len], '', 1)
                        num -= 1
                    data = data.replace(data[0:4], '', 1)
                if data[0:2] == '30':  # 自定义30数据
                    data = data.replace(data[0:46], '', 1)
                if data[0:2] == '32':  # 自定义32数据
                    data = data.replace(data[0:226], '', 1)
                if data[0:2] == '33':  # 医疗设备数据
                    data = data.replace(data[0:130], '', 1)
                continue
        # 保存
        worksheet.col(0).width = 256 * 20
        worksheet.col(1).width = 256 * 18
        workbook.save('./CAN_data.xls')
        file = open('./CAN_data.xls', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="CAN_data.xls"'
        return response


def zhu_download(request):
    if request.method == "GET":
        return render(request, 'zhu_download.html')
    if request.method == 'POST':
        stime = request.POST.get('stime')
        etime = request.POST.get('etime')
        car = Car.objects.filter(VIN='TLGF3D942JHL00002').first()
        cans = car.can_set.all().filter(Q(type=2 or 3) & Q(create_time__range=(stime, etime)))
        if not cans:
            result = {'error': '此时间段无数据,请重新输入!', 'stime': stime, 'etime': etime}
            return render(request, 'doctor_download.html', result)
        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        worksheet = workbook.add_sheet('整车数据信息')
        # 写入excel
        # 参数对应 行, 列, 值
        worksheet.write(0, 0, label='时间')
        worksheet.write(0, 1, label='ID')
        worksheet.write(0, 2, label='长度')
        worksheet.write(0, 3, label='数据')
        for i in range(len(cans)):
            message = cans[i].data
            data = message[60:-2]
            while data:
                if data[0:2] == '01':
                    data = data.replace(data[0:42], '', 1)
                if data[0:2] == '02':
                    len_m = 2 + int(data[2:4], 16) * 24
                    data = data.replace(data[0:2 + len_m], '', 1)
                if data[0:2] == '03':
                    data = data.replace(data[0:22], '', 1)
                if data[0:2] == '04':
                    data = data.replace(data[0:12], '', 1)
                if data[0:2] == '05':
                    data = data.replace(data[0:20], '', 1)
                if data[0:2] == '06':
                    data = data.replace(data[0:30], '', 1)
                if data[0:2] == '07':
                    data = data.replace(data[0:12], '', 1)
                    num1 = data[0:2]
                    if num1 != '00':
                        len1 = int(num1, 16) * 8
                        data = data.replace(data[0:2 + len1], '', 1)
                    else:
                        data = data.replace(data[0:2], '', 1)
                    num2 = data[0:2]
                    if num2 != '00':
                        len2 = int(num1, 16) * 8
                        data = data.replace(data[0:2 + len2], '', 1)
                    else:
                        data = data.replace(data[0:2], '', 1)
                    num3 = data[0:2]
                    if num3 != '00':
                        len3 = int(num1, 16) * 8
                        data = data.replace(data[0:2 + len3], '', 1)
                    else:
                        data = data.replace(data[0:2], '', 1)
                    num4 = data[0:2]
                    if num4 != '00':
                        len4 = int(num1, 16) * 8
                        data = data.replace(data[0:2 + len4], '', 1)
                    else:
                        data = data.replace(data[0:2], '', 1)
                if data[0:2] == '08':
                    num = int(data[2:4], 16)
                    while num != 0:
                        total_len = int(data[22:24], 16) * 4
                        data = data.replace(data[4:4 + 20 + total_len], '', 1)
                        num -= 1
                    data = data.replace(data[0:4], '', 1)
                if data[0:2] == '09':
                    num = int(data[2:4], 16)
                    while num != 0:
                        total_len = int(data[6:10], 16) * 2
                        data = data.replace(data[4:4 + 6 + total_len], '', 1)
                        num -= 1
                    data = data.replace(data[0:4], '', 1)
                if data[0:2] == '30':
                    data = data.replace(data[0:46], '', 1)
                if data[0:2] == '32':
                    time = cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S")
                    zhu = [data[i*2:(i+1)*2] for i in range(len(data)//2)]
                    worksheet.write(i * 14 + 1, 0, label=time)
                    worksheet.write(i * 14 + 1, 1, label='18FFA1F3')
                    worksheet.write(i * 14 + 1, 2, label='8')
                    worksheet.write(i * 14 + 1, 3, label=zhu[1] + ' ' + zhu[2] + ' ' + zhu[3] + ' ' + zhu[4] + ' ' + zhu[5] + ' ' + zhu[6] + ' ' + zhu[7] + ' ' + zhu[8])

                    worksheet.write(i * 14 + 2, 0, label=time)
                    worksheet.write(i * 14 + 2, 1, label='18FFA2F3')
                    worksheet.write(i * 14 + 2, 2, label='8')
                    worksheet.write(i * 14 + 2, 3, label=zhu[9] + ' ' + zhu[10] + ' ' + zhu[11] + ' ' + zhu[12] + ' ' + zhu[13] + ' ' + zhu[14] + ' ' + zhu[15] + ' ' + zhu[16])

                    worksheet.write(i * 14 + 3, 0, label=time)
                    worksheet.write(i * 14 + 3, 1, label='18FFA6F3')
                    worksheet.write(i * 14 + 3, 2, label='8')
                    worksheet.write(i * 14 + 3, 3, label=zhu[17] + ' ' + zhu[18] + ' ' + zhu[19] + ' ' + zhu[20] + ' ' + zhu[21] + ' ' + zhu[22] + ' ' + zhu[23] + ' ' + zhu[24])

                    worksheet.write(i * 14 + 4, 0, label=time)
                    worksheet.write(i * 14 + 4, 1, label='18FFA5F3')
                    worksheet.write(i * 14 + 4, 2, label='8')
                    worksheet.write(i * 14 + 4, 3, label=zhu[25] + ' ' + zhu[26] + ' ' + zhu[27] + ' ' + zhu[28] + ' ' + zhu[29] + ' ' + zhu[30] + ' ' + zhu[31] + ' ' + zhu[32])

                    worksheet.write(i * 14 + 5, 0, label=time)
                    worksheet.write(i * 14 + 5, 1, label='18FFA4F3')
                    worksheet.write(i * 14 + 5, 2, label='8')
                    worksheet.write(i * 14 + 5, 3, label=zhu[33] + ' ' + zhu[34] + ' ' + zhu[35] + ' ' + zhu[36] + ' ' + zhu[37] + ' ' + zhu[38] + ' ' + zhu[39] + ' ' + zhu[40])

                    worksheet.write(i * 14 + 6, 0, label=time)
                    worksheet.write(i * 14 + 6, 1, label='18FFAAF3')
                    worksheet.write(i * 14 + 6, 2, label='8')
                    worksheet.write(i * 14 + 6, 3, label=zhu[41] + ' ' + zhu[42] + ' ' + zhu[43] + ' ' + zhu[44] + ' ' + zhu[45] + ' ' + zhu[46] + ' ' + zhu[47] + ' ' + zhu[48])

                    worksheet.write(i * 14 + 7, 0, label=time)
                    worksheet.write(i * 14 + 7, 1, label='18FF45F3')
                    worksheet.write(i * 14 + 7, 2, label='8')
                    worksheet.write(i * 14 + 7, 3, label=zhu[49] + ' ' + zhu[50] + ' ' + zhu[51] + ' ' + zhu[52] + ' ' + zhu[53] + ' ' + zhu[54] + ' ' + zhu[55] + ' ' + zhu[56])

                    worksheet.write(i * 14 + 8, 0, label=time)
                    worksheet.write(i * 14 + 8, 1, label='18FFF345')
                    worksheet.write(i * 14 + 8, 2, label='8')
                    worksheet.write(i * 14 + 8, 3, label=zhu[57] + ' ' + zhu[58] + ' ' + zhu[59] + ' ' + zhu[60] + ' ' + zhu[61] + ' ' + zhu[62] + ' ' + zhu[63] + ' ' + zhu[64])

                    worksheet.write(i * 14 + 9, 0, label=time)
                    worksheet.write(i * 14 + 9, 1, label='18000AD1')
                    worksheet.write(i * 14 + 9, 2, label='8')
                    worksheet.write(i * 14 + 9, 3, label=zhu[65] + ' ' + zhu[66] + ' ' + zhu[67] + ' ' + zhu[68] + ' ' + zhu[69] + ' ' + zhu[70] + ' ' + zhu[71] + ' ' + zhu[72])

                    worksheet.write(i * 14 + 10, 0, label=time)
                    worksheet.write(i * 14 + 10, 1, label='18000BD1')
                    worksheet.write(i * 14 + 10, 2, label='8')
                    worksheet.write(i * 14 + 10, 3, label=zhu[73] + ' ' + zhu[74] + ' ' + zhu[75] + ' ' + zhu[76] + ' ' + zhu[77] + ' ' + zhu[78] + ' ' + zhu[79] + ' ' + zhu[80])

                    worksheet.write(i * 14 + 11, 0, label=time)
                    worksheet.write(i * 14 + 11, 1, label='18000CD1')
                    worksheet.write(i * 14 + 11, 2, label='8')
                    worksheet.write(i * 14 + 11, 3, label=zhu[81] + ' ' + zhu[82] + ' ' + zhu[83] + ' ' + zhu[84] + ' ' + zhu[85] + ' ' + zhu[86] + ' ' + zhu[87] + ' ' + zhu[88])

                    worksheet.write(i * 14 + 12, 0, label=time)
                    worksheet.write(i * 14 + 12, 1, label='18F00503')
                    worksheet.write(i * 14 + 12, 2, label='8')
                    worksheet.write(i * 14 + 12, 3, label=zhu[89] + ' ' + zhu[90] + ' ' + zhu[91] + ' ' + zhu[92] + ' ' + zhu[93] + ' ' + zhu[94] + ' ' + zhu[95] + ' ' + zhu[96])

                    worksheet.write(i * 14 + 13, 0, label=time)
                    worksheet.write(i * 14 + 13, 1, label='0CFE6CEE')
                    worksheet.write(i * 14 + 13, 2, label='8')
                    worksheet.write(i * 14 + 13, 3, label=zhu[97] + ' ' + zhu[98] + ' ' + zhu[99] + ' ' + zhu[100] + ' ' + zhu[101] + ' ' + zhu[102] + ' ' + zhu[103] + ' ' + zhu[104])

                    worksheet.write(i * 14 + 14, 0, label=time)
                    worksheet.write(i * 14 + 14, 1, label='18FEE017')
                    worksheet.write(i * 14 + 14, 2, label='8')
                    worksheet.write(i * 14 + 14, 3, label=zhu[105] + ' ' + zhu[106] + ' ' + zhu[107] + ' ' + zhu[108] + ' ' + zhu[109] + ' ' + zhu[110] + ' ' + zhu[111] + ' ' + zhu[112])
                    data = data.replace(data[0:226], '', 1)
                if data[0:2] == '33':
                    data = data.replace(data[0:130], '', 1)
                continue
        worksheet.col(0).width = 256 * 20
        worksheet.col(1).width = 256 * 18
        workbook.save('./zhu_data.xls')
        file = open('./zhu_data.xls', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="zhu_data.xls"'
        return response
