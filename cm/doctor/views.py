import time

import xlwt
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket
from django_redis import get_redis_connection


# Create your views here.
from car.models import Car


def doctor(request):
    if request.method == 'GET':
        return render(request, 'doctor.html')


@accept_websocket
def drug_socket(request):
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


def analysis_doctor(request):
    data = request.GET.get('data')
    return render(request, 'analysis_doctor.html', {'data': data})


def doctor_download(request):
    if request.method == "GET":
        return render(request, 'doctor_download.html')
    if request.method == 'POST':
        VIN = request.POST.get('VIN')
        stime = request.POST.get('stime')
        etime = request.POST.get('etime')
        car = Car.objects.filter(VIN=VIN, dept='医疗').first()
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
        worksheet = workbook.add_sheet('医疗设备信息')
        # 写入excel
        # 参数对应 行, 列, 值
        worksheet.write(0, 0, label='VIN码')
        worksheet.write(0, 1, label='Date')
        worksheet.write(0, 2, label='PackVolt_Bef')
        worksheet.write(0, 3, label='PackVolt_Aft')
        worksheet.write(0, 4, label='PackVolt_Chg')
        worksheet.write(0, 5, label='PackCellSumvolt')
        worksheet.write(0, 6, label='MaxCellTemp')
        worksheet.write(0, 7, label='MinCellTemp')
        worksheet.write(0, 8, label='MaxCellTempID')
        worksheet.write(0, 9, label='MinCellTempID')
        worksheet.write(0, 10, label='Temp_Number')
        worksheet.write(0, 11, label='AvgCellTemp')
        worksheet.write(0, 12, label='MaxCellVolt')
        worksheet.write(0, 13, label='MinCellVolt')
        worksheet.write(0, 14, label='AvgCellVolt')
        worksheet.write(0, 15, label='MaxCellVoltID')
        worksheet.write(0, 16, label='MinCellVoltID')
        worksheet.write(0, 17, label='Abs_cur')
        worksheet.write(0, 18, label='RealSoc')
        worksheet.write(0, 19, label='Iso_Res_Val')
        worksheet.write(0, 20, label='SocGetChgMahSum')
        worksheet.write(0, 21, label='SocGetDischgMahSum')
        worksheet.write(0, 22, label='Rest_Mah')
        worksheet.write(0, 23, label='Pack_Available_Mah')
        worksheet.write(0, 24, label='Curr_Mwh')
        worksheet.write(0, 25, label='BMS_RATED_ENERGY_WH')
        worksheet.write(0, 26, label='BMS_RATED_VOLT')
        worksheet.write(0, 27, label='SOC_PACK_NOMINAL_AH')
        worksheet.write(0, 28, label='RelayControl_State')
        worksheet.write(0, 29, label='MainRlyState_flg')
        worksheet.write(0, 30, label='DchgFaultLevel')
        worksheet.write(0, 31, label='ChgFaultLevel')
        worksheet.write(0, 32, label='ChargeRlyState_flg')
        worksheet.write(0, 33, label='BMS_WorkSt')
        worksheet.write(0, 34, label='BatOthFltList')
        worksheet.write(0, 35, label='BatOthFltNum')
        worksheet.write(0, 36, label='BMS_Sw_Major')
        worksheet.write(0, 37, label='BMS_Sw_Minor')
        worksheet.write(0, 38, label='BMS_Sw_Build')
        worksheet.write(0, 39, label='BMS_Hw_Major')
        worksheet.write(0, 40, label='BMS_Hw_Minor')
        worksheet.write(0, 41, label='BMS_Hw_Build')
        worksheet.write(0, 42, label='BMS_Month')
        worksheet.write(0, 43, label='BMS_Date')
        worksheet.write(0, 44, label='CellVolt_01')
        worksheet.write(0, 45, label='CellVolt_02')
        worksheet.write(0, 46, label='CellVolt_03')
        worksheet.write(0, 47, label='CellVolt_04')
        worksheet.write(0, 48, label='CellVolt_05')
        worksheet.write(0, 49, label='CellVolt_06')
        worksheet.write(0, 50, label='CellVolt_07')
        worksheet.write(0, 51, label='CellVolt_08')
        worksheet.write(0, 52, label='CellVolt_09')
        worksheet.write(0, 53, label='CellVolt_10')
        worksheet.write(0, 54, label='CellVolt_11')
        worksheet.write(0, 55, label='CellVolt_12')
        worksheet.write(0, 56, label='CellVolt_13')
        worksheet.write(0, 57, label='CellVolt_14')
        worksheet.write(0, 58, label='CellVolt_15')
        worksheet.write(0, 59, label='CellVolt_16')
        worksheet.write(0, 60, label='CellVolt_17')
        worksheet.write(0, 61, label='CellVolt_18')
        worksheet.write(0, 62, label='CellVolt_19')
        worksheet.write(0, 63, label='CellVolt_20')
        worksheet.write(0, 64, label='CellVolt_21')
        worksheet.write(0, 65, label='CellVolt_22')
        worksheet.write(0, 66, label='CellVolt_23')
        worksheet.write(0, 67, label='CellVolt_24')
        worksheet.write(0, 68, label='CellVolt_25')
        worksheet.write(0, 69, label='CellVolt_26')
        worksheet.write(0, 70, label='CellVolt_27')
        worksheet.write(0, 71, label='CellVolt_28')
        worksheet.write(0, 72, label='CellVolt_29')
        worksheet.write(0, 73, label='CellVolt_30')
        worksheet.write(0, 74, label='CellVolt_31')
        worksheet.write(0, 75, label='CellVolt_32')
        worksheet.write(0, 76, label='CellVolt_33')
        worksheet.write(0, 77, label='CellVolt_34')
        worksheet.write(0, 78, label='CellVolt_35')
        worksheet.write(0, 79, label='CellVolt_36')
        worksheet.write(0, 80, label='CellVolt_37')
        worksheet.write(0, 81, label='CellVolt_38')
        worksheet.write(0, 82, label='CellVolt_39')
        worksheet.write(0, 83, label='CellVolt_40')
        worksheet.write(0, 84, label='CellVolt_41')
        worksheet.write(0, 85, label='CellVolt_42')
        worksheet.write(0, 86, label='CellVolt_43')
        worksheet.write(0, 87, label='CellVolt_44')
        worksheet.write(0, 88, label='CellVolt_45')
        worksheet.write(0, 89, label='CellVolt_46')
        worksheet.write(0, 90, label='CellVolt_47')
        worksheet.write(0, 91, label='CellVolt_48')
        worksheet.write(0, 92, label='CellVolt_49')
        worksheet.write(0, 93, label='CellVolt_50')
        worksheet.write(0, 94, label='CellVolt_51')
        worksheet.write(0, 95, label='CellVolt_52')
        worksheet.write(0, 96, label='CellVolt_53')
        worksheet.write(0, 97, label='CellVolt_54')
        worksheet.write(0, 98, label='CellVolt_55')
        worksheet.write(0, 99, label='CellVolt_56')
        worksheet.write(0, 100, label='CellVolt_57')
        worksheet.write(0, 101, label='CellVolt_58')
        worksheet.write(0, 102, label='CellVolt_59')
        worksheet.write(0, 103, label='CellVolt_60')
        worksheet.write(0, 104, label='CellVolt_61')
        worksheet.write(0, 105, label='CellVolt_62')
        worksheet.write(0, 106, label='CellVolt_63')
        worksheet.write(0, 107, label='CellVolt_64')
        worksheet.write(0, 108, label='CellVolt_65')
        worksheet.write(0, 109, label='CellVolt_66')
        worksheet.write(0, 110, label='CellVolt_67')
        worksheet.write(0, 111, label='CellVolt_68')
        worksheet.write(0, 112, label='CellVolt_69')
        worksheet.write(0, 113, label='CellVolt_70')
        worksheet.write(0, 114, label='CellVolt_71')
        worksheet.write(0, 115, label='CellVolt_72')
        worksheet.write(0, 116, label='CellTempr_01')
        worksheet.write(0, 117, label='CellTempr_02')
        worksheet.write(0, 118, label='CellTempr_03')
        worksheet.write(0, 119, label='CellTempr_04')
        worksheet.write(0, 120, label='CellTempr_05')
        worksheet.write(0, 121, label='CellTempr_06')
        worksheet.write(0, 122, label='CellTempr_07')
        worksheet.write(0, 123, label='CellTempr_08')
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
            worksheet.write(i+1, 0, label=VIN)
            worksheet.write(i+1, 1, label=cans[i].ter_time.strftime("%Y-%m-%d %H:%M:%S"))
            while data:
                if data[0:2] == '01':  # 整车数据
                    data = data.replace(data[0:42], '', 1)
                if data[0:2] == '02':  # 驱动电机数据
                    len_m = 2 + int(data[2:4], 16) * 24
                    data = data.replace(data[0:2 + len_m], '', 1)
                if data[0:2] == '03':
                    data = data.replace(data[0:22], '', 1)
                if data[0:2] == '04':
                    data = data.replace(data[0:12], '', 1)
                if data[0:2] == '05':
                    if data[2:4] == '00':
                        longitude = int(data[4:12], 16) / 1000000
                        latitude = int(data[12:20], 16) / 1000000
                    data = data.replace(data[0:20], '', 1)
                if data[0:2] == '06':
                    # 0601250fd001010fa3010248010728  极值数据
                    limit = [data[i*2:(i+1)*2] for i in range(len(data)//2)]
                    worksheet.write(i + 1, 6, label=(int(limit[11], 16) - 40))  # 单体最高温度
                    worksheet.write(i + 1, 7, label=(int(limit[14], 16) - 40))  # 单体最低温度
                    worksheet.write(i + 1, 8, label=int(limit[10], 16))  # 单体最高温度位置
                    worksheet.write(i + 1, 9, label=int(limit[13], 16))  # 单体最低温度位置
                    worksheet.write(i+1, 12, label=(int(limit[3], 16)*256+int(limit[4], 16))/1000)  # 单体最高电压
                    worksheet.write(i+1, 13, label=(int(limit[7], 16)*256+int(limit[8], 16))/1000)  # 单体最低电压
                    worksheet.write(i+1, 15, label=int(limit[2], 16))  # 单体最高电压位置
                    worksheet.write(i+1, 16, label=int(limit[6], 16))  # 单体最低电压位置
                    data = data.replace(data[0:30], '', 1)
                if data[0:2] == '07':
                    if data[2:4] == '00':
                        pass
                    else:
                        print('车辆报警')
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
                if data[0:2] == '08':  # 电池电压数据
                    num = int(data[2:4], 16)
                    while num != 0:
                        num_battery = int(data[22:24], 16)
                        for b in range(0, num_battery):
                            v = int(data[24 + 4 * b: 24 + 4 * (b + 1)], 16)/1000
                            worksheet.write(i+1, 44+b, label=v)
                        total_len = num_battery * 4
                        data = data.replace(data[4: 4 + 20 + total_len], '', 1)
                        num -= 1
                    data = data.replace(data[0:4], '', 1)
                if data[0:2] == '09':  # 电池温度数据
                    # 09010100084448464547462828  温度数据
                    num = int(data[2:4], 16)
                    while num != 0:
                        num_temp = int(data[6:10], 16)
                        for c in range(0, num_temp):
                            C = int(data[10 + 2*c: 10 + 2 * (c+1)], 16) - 40
                            worksheet.write(i+1, 116+c, label=C)
                        total_len = num_temp * 2
                        data = data.replace(data[4:4 + 6 + total_len], '', 1)
                        num -= 1
                    data = data.replace(data[0:4], '', 1)
                if data[0:2] == '30':  # 自定义30数据
                    data = data.replace(data[0:46], '', 1)
                if data[0:2] == '32':  # 自定义32数据
                    data = data.replace(data[0:226], '', 1)
                if data[0:2] == '33':  # 医疗设备数据
                    # 3346060fbd271003b227222710000000840000005d000034d100003dcc03e8151f0a68000f09070000012701010000030000030902037d03b20b520b52037d0b55  医疗设备数据
                    lis = [data[i*2:(i+1)*2] for i in range(len(data)//2)]
                    worksheet.write(i+1, 2, label=((int(lis[57], 16)*256)+int(lis[58], 16))/10)  # 电池包内压
                    worksheet.write(i+1, 3, label=((int(lis[59], 16)*256)+int(lis[60], 16))/10)  # 电池包外压
                    worksheet.write(i+1, 4, label=((int(lis[61], 16)*256)+int(lis[62], 16))/10)  # 充电器电压
                    worksheet.write(i+1, 5, label=((int(lis[63], 16)*256)+int(lis[64], 16))/10)  # 单体电压总和
                    worksheet.write(i+1, 10, label=int(lis[2], 16))  # 温度传感器数量
                    worksheet.write(i+1, 11, label=int(lis[1], 16)-40)  # 单体平均温度
                    worksheet.write(i+1, 14, label=(int(lis[3], 16)*256+int(lis[4], 16))/1000)  # 单体平均电压
                    worksheet.write(i+1, 17, label=(((int(lis[5], 16)*256)+int(lis[6], 16))-10000)/10)  # 传感器电流值
                    worksheet.write(i+1, 18, label=((int(lis[53], 16)*256)+int(lis[54], 16))/10)  # 真实SOC
                    worksheet.write(i+1, 19, label=((int(lis[9], 16)*256)+int(lis[10], 16)))  # 绝缘阻值
                    worksheet.write(i+1, 20, label=((int(lis[13], 16)*256*256*256)+(int(lis[14], 16)*256*256)+(int(lis[15], 16)*256)+int(lis[16], 16)))  # 总充电安时数
                    worksheet.write(i+1, 21, label=((int(lis[17], 16)*256*256*256)+(int(lis[18], 16)*256*256)+(int(lis[19], 16)*256)+int(lis[20], 16)))  # 总放电安时数
                    worksheet.write(i+1, 22, label=((int(lis[21], 16)*256*256*256)+(int(lis[22], 16)*256*256)+(int(lis[23], 16)*256)+int(lis[24], 16))/1000)  # 剩余容量
                    worksheet.write(i+1, 23, label=((int(lis[25], 16)*256*256*256)+(int(lis[26], 16)*256*256)+(int(lis[27], 16)*256)+int(lis[28], 16))/1000)  # 额定容量
                    worksheet.write(i+1, 24, label=(int(lis[29], 16)*256)+int(lis[30], 16))  # 当前瓦时
                    worksheet.write(i+1, 25, label=(int(lis[31], 16)*256)+int(lis[32], 16))  # 额定瓦时
                    worksheet.write(i+1, 26, label=((int(lis[33], 16)*256)+int(lis[34], 16))/10)  # 额定电压
                    worksheet.write(i+1, 27, label=(int(lis[35], 16)*256)+int(lis[36], 16))  # 额定安时
                    worksheet.write(i+1, 28, label=int(lis[38], 16))  # 继电器状态
                    worksheet.write(i+1, 29, label=int(lis[43], 16))  # 主正继电器闭合状态
                    worksheet.write(i+1, 30, label=int(lis[39], 16))  # 放电状态故障等级
                    worksheet.write(i+1, 31, label=int(lis[40], 16))  # 充电状态故障等级
                    worksheet.write(i+1, 32, label=int(lis[44], 16))  # 充电继电器闭合状态
                    worksheet.write(i+1, 33, label=int(lis[37], 16))  # BMS工作状态
                    worksheet.write(i+1, 34, label=int(lis[42], 16))  # 故障序号
                    worksheet.write(i+1, 35, label=int(lis[41], 16))  # 故障数量
                    worksheet.write(i+1, 36, label=int(lis[45], 16))  # 主软件版本号
                    worksheet.write(i+1, 37, label=int(lis[46], 16))  # 辅软件版本号
                    worksheet.write(i+1, 38, label=int(lis[47], 16))  # 软件版本号
                    worksheet.write(i+1, 39, label=int(lis[48], 16))  # 主硬件版本号
                    worksheet.write(i+1, 40, label=int(lis[49], 16))  # 辅硬件版本号
                    worksheet.write(i+1, 41, label=int(lis[50], 16))  # 硬件版本号
                    worksheet.write(i+1, 42, label=int(lis[51], 16))  # 月份
                    worksheet.write(i+1, 43, label=int(lis[52], 16))  # 日期
                    data = data.replace(data[0:130], '', 1)
                continue
        # 保存
        worksheet.col(0).width = 256 * 20
        worksheet.col(1).width = 256 * 18
        workbook.save('./doctor_data.xls')
        file = open('./doctor_data.xls', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="doctor_data.xls"'
        return response
