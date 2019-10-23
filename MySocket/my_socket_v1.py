import base64
import socket
from threading import Thread, Timer
import datetime
import pymysql
import redis
import time

import requests


def main():
    def translate(longitude, latitude):
        """
        经纬度转换
        :param longitude: 经度
        :param latitude: 纬度
        :return:
        """
        url = 'http://api.map.baidu.com/ag/coord/convert?from=0&to=4&x=%f&y=%f' % (longitude, latitude)
        response = requests.get(url)
        data = response.json()
        longitude = data['x']
        latitude = data['y']
        res = base64.b64decode(longitude)
        longitude = res.decode()
        res = base64.b64decode(latitude)
        latitude = res.decode()
        return (longitude, latitude)

    def BCC(q):
        """
        BCC异或校验法
        :param q:
        :return: 16进制数
        """
        sum = 0
        for i in range(2, len(q), 2):
            sum = int(hex(sum ^ int(q[i-2:i], 16)), 16)
        result = hex(sum)[2:]
        if len(result) == 1:
            return '0' + result
        return result

    def BCC_all(q):
        """
        BCC异或校验法
        :param q:
        :return: 16进制数
        """
        sum = 0
        for i in range(2, len(q)+2, 2):
            sum = int(hex(sum ^ int(q[i-2:i], 16)), 16)
        result = hex(sum)[2:]
        if len(result) == 1:
            return '0' + result
        return result

    class Convertertime():
        """
        时间转换
        """
        @staticmethod
        def to_hex_time():
            """
            转16进制时间串
            :return:
            """
            t = time.localtime(time.time())
            year = hex(int(str(t[0])[2:]))[2:]
            month = '0' + hex(t[1])[2:]
            day = hex(t[2])[2:]
            hour = hex(t[3])[2:]
            mini = hex(t[4])[2:]
            second = hex(t[5])[2:]
            if len(day) == 1:
                day = '0' + day
            if len(hour) == 1:
                hour = '0' + hour
            if len(mini) == 1:
                mini = '0' + mini
            if len(second) == 1:
                second = '0' + second
            now = year + month + day + hour + mini + second
            return now

        @staticmethod
        def to_time(t):
            """
            16进制转10进制时间
            :param t:
            :return:
            """
            lis = [str(int(t[i:i + 2], 16)) for i in range(0, len(t), 2)]
            return '20' + lis[0] + '-' + lis[1] + '-' + lis[2] + ' ' + lis[3] + ':' + lis[4] + ':' + lis[5]

    class Converter(object):
        """
        自定义ASCII码转换
        """
        @staticmethod
        def to_ascii(h):
            list_s = [chr(int(h[i:i + 2], 16)) for i in range(0, len(h), 2)]
            return ''.join(list_s)

        @staticmethod
        def to_hex(s):
            e = 0
            for i in s:
                d = ord(i)
                e = e * 256 + d
            return '%x' % e

    class CarTransHandle(Thread):
        """
        自定义线程类
        """
        is_break = True
        is_login = False

        def __init__(self, cclient):
            super().__init__()
            self.cclient = cclient

        def run(self):
            try:
                message = ''
                self.cclient.settimeout(60)
                while True:
                    data = Converter().to_hex('L' + self.cclient.recv(2048).decode('raw_unicode_escape'))
                    data = data[2:]
                    message += data
                    print(message)
                    if not self.is_break or not data:
                        print('tcp连接中断,last_message:', last_message)
                        try:
                            VIN = Converter().to_ascii(last_message[8:42])
                            r.zrem("car_login", VIN)
                            location = r.geopos('car_online', VIN)
                            r.zrem("car_online", VIN)
                            r.geoadd('car_offline', location[0][0], location[0][1], VIN)
                        except:
                            print('车辆正常离线出错')
                            break
                        break
                    if message[:4] != '2323':
                        print('无2323')
                        break
                    if len(message) < 50:
                        print('接收一条信息不完整')
                        continue
                    len_data = int(message[44:48], 16)
                    if len(message) < 48 + len_data*2 + 2:
                        print('接收一条大于50长度信息不完整')
                        continue
                    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    while True:
                        if not message:
                            break
                        if len(message) < 50:
                            print('处理一条信息不完整')
                            break
                        len_data = int(message[44:48], 16)
                        if len(message) < 48 + len_data * 2 + 2:
                            print('处理一条大于50长度信息不完整')
                            break
                        last_message = message
                        if message[4:6] == '01':
                            print('车辆登入')
                            len_data = int(message[44:48], 16)
                            info = message[:48+len_data*2+2]
                            if BCC(info) != info[-2:]:
                                print(info)
                                print('BCC校验失败')
                                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                     db='cm',
                                                     charset='utf8')
                                cursor = db.cursor()
                                VIN = Converter().to_ascii(info[8:42])
                                sql = 'select * from car where VIN = "%s";' % VIN
                                cursor.execute(sql)
                                car = cursor.fetchone()
                                cursor.close()
                                db.close()
                                car_ID = car[0]
                                ter_time = Convertertime().to_time(info[48:60])
                                type = 1002
                                messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                                data = info[:6] + '02' + info[8:42] + '010006' + Convertertime().to_hex_time()
                                my_bcc = BCC_all(data)
                                self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                                message = ''
                                break
                            message = message.replace(info, '', 1)
                            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475', db='cm',
                                                 charset='utf8')
                            cursor = db.cursor()
                            VIN = Converter().to_ascii(info[8:42])
                            sql = 'select * from car where VIN = "%s";' % VIN
                            cursor.execute(sql)
                            car = cursor.fetchone()
                            cursor.close()
                            db.close()
                            ter_time = Convertertime().to_time(info[48:60])
                            if not car:
                                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                     db='cm',
                                                     charset='utf8')
                                cursor = db.cursor()
                                ICCID = Converter().to_ascii(info[64:104])
                                sql = 'select * from machine where ICCID = "%s";' % ICCID
                                cursor.execute(sql)
                                car_ICCID = cursor.fetchone()
                                cursor.close()
                                db.close()
                                if not car_ICCID:
                                    # type = 1003
                                    # messages['CAN'].append((1, create_time, ter_time, info, type))
                                    data = info[:6] + '02' + info[8:42] + '010006' + Convertertime().to_hex_time()
                                    my_bcc = BCC_all(data)
                                    self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                                    print('车辆登录失败')
                                    self.is_break = False
                                    break
                                else:
                                    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                         db='cm',
                                                         charset='utf8')
                                    cursor = db.cursor()
                                    VIN = Converter().to_ascii(info[8:42])
                                    query = "insert into car(VIN,dept,create_time) VALUES ('%s', '%s', '%s')" % (VIN, car_ICCID[5], ter_time)
                                    cursor.execute(query)
                                    db.commit()
                                    sql = 'select * from car where VIN = "%s";' % VIN
                                    cursor.execute(sql)
                                    car = cursor.fetchone()
                                    cursor.close()
                                    db.close()
                            car_ID = car[0]
                            type = 1
                            messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                            data = info[:6] + '01' + info[8:42] + '010006' + Convertertime().to_hex_time()
                            my_bcc = BCC_all(data)
                            self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                            self.is_login = True
                            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                 db='cm',
                                                 charset='utf8')
                            cursor = db.cursor()
                            query = "update car set ICCID = '%s' where id = %d;" % (Converter().to_ascii(info[64:104]), car[0])
                            cursor.execute(query)
                            db.commit()
                            cursor.close()
                            db.close()
                            r.zadd('car_login', {VIN: 0})
                            continue
                        if message[4:6] == '02':
                            print('实时信息上报')
                            len_data = int(message[44:48], 16)
                            info = message[:48 + len_data * 2 + 2]
                            if BCC(info) != info[-2:]:
                                print(info)
                                print('BCC校验失败')
                                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                     db='cm',
                                                     charset='utf8')
                                cursor = db.cursor()
                                VIN = Converter().to_ascii(info[8:42])
                                sql = 'select * from car where VIN = "%s";' % VIN
                                cursor.execute(sql)
                                car = cursor.fetchone()
                                cursor.close()
                                db.close()
                                car_ID = car[0]
                                ter_time = Convertertime().to_time(info[48:60])
                                type = 1002
                                messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                                data = info[:6] + '02' + info[8:42] + '010006' + Convertertime().to_hex_time()
                                my_bcc = BCC_all(data)
                                self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                                message = ''
                                break
                            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475', db='cm',
                                                 charset='utf8')
                            cursor = db.cursor()
                            VIN = Converter().to_ascii(info[8:42])
                            sql = 'select * from car where VIN = "%s";' % VIN
                            cursor.execute(sql)
                            car = cursor.fetchone()
                            cursor.close()
                            db.close()
                            car_ID = car[0]
                            ter_time = Convertertime().to_time(info[48:60])
                            type = 2
                            messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                            data = info[60:-2]
                            message = message.replace(info, '', 1)
                            try:
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
                                        if data[2:4] == '00':
                                            longitude = int(data[4:12], 16) / 1000000
                                            latitude = int(data[12:20], 16) / 1000000
                                            messages['online'].append(translate(longitude, latitude) + (VIN, ter_time))
                                        data = data.replace(data[0:20], '', 1)
                                    if data[0:2] == '06':
                                        data = data.replace(data[0:30], '', 1)
                                    if data[0:2] == '07':
                                        if data[2:4] == '00':
                                            messages['unwarning'].append(VIN)
                                        else:
                                            print('车辆报警')
                                            messages['warning'].append(VIN)
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
                                        print('自定义30数据')
                                        data = data.replace(data[0:46], '', 1)
                                    if data[0:2] == '32':
                                        print('自定义32数据')
                                        data = data.replace(data[0:226], '', 1)
                                    if data[0:2] == '33':
                                        print('医疗设备数据')
                                        data = data.replace(data[0:130], '', 1)
                                continue
                            except:
                                print('上报信息错误')
                                type = 1001
                                messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                                message = ''
                                break
                        if message[4:6] == '03':
                            print('补发信息上报')
                            len_data = int(message[44:48], 16)
                            info = message[:48 + len_data * 2 + 2]
                            if BCC(info) != info[-2:]:
                                print(info)
                                print('BCC校验失败')
                                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                     db='cm',
                                                     charset='utf8')
                                cursor = db.cursor()
                                VIN = Converter().to_ascii(info[8:42])
                                sql = 'select * from car where VIN = "%s";' % VIN
                                cursor.execute(sql)
                                car = cursor.fetchone()
                                cursor.close()
                                db.close()
                                car_ID = car[0]
                                ter_time = Convertertime().to_time(info[48:60])
                                type = 1002
                                messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                                data = info[:6] + '02' + info[8:42] + '010006' + Convertertime().to_hex_time()
                                my_bcc = BCC_all(data)
                                self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                                message = ''
                                break
                            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475', db='cm',
                                                 charset='utf8')
                            cursor = db.cursor()
                            VIN = Converter().to_ascii(info[8:42])
                            sql = 'select * from car where VIN = "%s";' % VIN
                            cursor.execute(sql)
                            car = cursor.fetchone()
                            cursor.close()
                            db.close()
                            car_ID = car[0]
                            ter_time = Convertertime().to_time(info[48:60])
                            type = 3
                            messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                            data = info[60:-2]
                            message = message.replace(info, '', 1)
                            try:
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
                                        if data[2:4] == '00':
                                            longitude = int(data[4:12], 16) / 1000000
                                            latitude = int(data[12:20], 16) / 1000000
                                            messages['online'].append(translate(longitude, latitude) + (VIN, ter_time))
                                        data = data.replace(data[0:20], '', 1)
                                    if data[0:2] == '06':
                                        data = data.replace(data[0:30], '', 1)
                                    if data[0:2] == '07':
                                        if data[2:4] == '00':
                                            messages['unwarning'].append(VIN)
                                        else:
                                            print('车辆报警')
                                            messages['warning'].append(VIN)
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
                                        print('自定义30数据')
                                        data = data.replace(data[0:46], '', 1)
                                    if data[0:2] == '32':
                                        print('自定义32数据')
                                        data = data.replace(data[0:226], '', 1)
                                    if data[0:2] == '33':
                                        print('医疗设备数据')
                                        data = data.replace(data[0:130], '', 1)
                                continue
                            except:
                                print('上报信息错误')
                                type = 1001
                                messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                                message = ''
                                break
                        if message[4:6] == '04':
                            self.is_break = False
                            print('车辆登出')
                            len_data = int(message[44:48], 16)
                            info = message[:48 + len_data * 2 + 2]
                            if BCC(info) != info[-2:]:
                                print(info)
                                print('BCC校验失败')
                                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                     db='cm',
                                                     charset='utf8')
                                cursor = db.cursor()
                                VIN = Converter().to_ascii(info[8:42])
                                sql = 'select * from car where VIN = "%s";' % VIN
                                cursor.execute(sql)
                                car = cursor.fetchone()
                                cursor.close()
                                db.close()
                                car_ID = car[0]
                                ter_time = Convertertime().to_time(info[48:60])
                                type = 1002
                                messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                                data = info[:6] + '02' + info[8:42] + '010006' + Convertertime().to_hex_time()
                                my_bcc = BCC_all(data)
                                self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                                message = ''
                                break
                            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475', db='cm',
                                                 charset='utf8')
                            cursor = db.cursor()
                            VIN = Converter().to_ascii(info[8:42])
                            sql = 'select * from car where VIN = "%s";' % VIN
                            cursor.execute(sql)
                            car = cursor.fetchone()
                            cursor.close()
                            db.close()
                            car_ID = car[0]
                            ter_time = Convertertime().to_time(info[48:60])
                            type = 4
                            messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                            break
                        if message[4:6] == '07':
                            len_data = int(message[44:48], 16)
                            info = message[:48 + len_data * 2 + 2]
                            message = message.replace(info, '', 1)
                            if BCC(info) != info[-2:]:
                                print(info)
                                print('BCC校验失败')
                                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                     db='cm',
                                                     charset='utf8')
                                cursor = db.cursor()
                                VIN = Converter().to_ascii(info[8:42])
                                sql = 'select * from car where VIN = "%s";' % VIN
                                cursor.execute(sql)
                                car = cursor.fetchone()
                                cursor.close()
                                db.close()
                                car_ID = car[0]
                                ter_time = Convertertime().to_time(info[48:60])
                                type = 1002
                                messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                                data = info[:6] + '02' + info[8:42] + '010006' + Convertertime().to_hex_time()
                                my_bcc = BCC_all(data)
                                self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                                message = ''
                                break
                            data = info[:6] + '01' + info[8:42] + '010006' + Convertertime().to_hex_time()
                            my_bcc = BCC_all(data)
                            self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                            if self.is_login:
                                VIN = Converter().to_ascii(info[8:42])
                                num = r.zscore('car', VIN)
                                if num:
                                    if int(num) == 1:
                                        print('锁车命令发出')
                                        data = '232382fe' + info[8:42] + '010008' + Convertertime().to_hex_time() + '9091'
                                        my_bcc = BCC_all(data)
                                        self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                                    if int(num) == 2:
                                        print('解锁命令发出')
                                        data = '232382fe' + info[8:42] + '010008' + Convertertime().to_hex_time() + '9090'
                                        my_bcc = BCC_all(data)
                                        self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                                    score_c = r.zscore('car_status', VIN)
                                    if int(score_c) == 3:
                                        print('车辆状态查询')
                                        data = '232380fe' + info[8:42] + '010008' + Convertertime().to_hex_time() + '0190'
                                        my_bcc = BCC_all(data)
                                        self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                            continue
                        if message[4:6] == '08':
                            print('校时')
                            len_data = int(message[44:48], 16)
                            info = message[:48 + len_data * 2 + 2]
                            if BCC(info) != info[-2:]:
                                print(info)
                                print('BCC校验失败')
                                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                     db='cm',
                                                     charset='utf8')
                                cursor = db.cursor()
                                VIN = Converter().to_ascii(info[8:42])
                                sql = 'select * from car where VIN = "%s";' % VIN
                                cursor.execute(sql)
                                car = cursor.fetchone()
                                cursor.close()
                                db.close()
                                car_ID = car[0]
                                ter_time = Convertertime().to_time(info[48:60])
                                type = 1002
                                messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                                data = info[:6] + '02' + info[8:42] + '010006' + Convertertime().to_hex_time()
                                my_bcc = BCC_all(data)
                                self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                                message = ''
                                break
                            message = message.replace(info, '', 1)
                            data = info[:6] + '01' + info[8:42] + '010006' + Convertertime().to_hex_time()
                            my_bcc = BCC_all(data)
                            self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                            continue
                        if message[4:6] == '80':
                            len_data = int(message[44:48], 16)
                            info = message[:48 + len_data * 2 + 2]
                            if BCC(info) != info[-2:]:
                                print(info)
                                print('BCC校验失败')
                                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                     db='cm',
                                                     charset='utf8')
                                cursor = db.cursor()
                                VIN = Converter().to_ascii(info[8:42])
                                sql = 'select * from car where VIN = "%s";' % VIN
                                cursor.execute(sql)
                                car = cursor.fetchone()
                                cursor.close()
                                db.close()
                                car_ID = car[0]
                                ter_time = Convertertime().to_time(info[48:60])
                                type = 1002
                                messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                                data = info[:6] + '02' + info[8:42] + '010006' + Convertertime().to_hex_time()
                                my_bcc = BCC_all(data)
                                self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                                message = ''
                                break
                            message = message.replace(info, '', 1)
                            if info[62:64] == '90':
                                print('车辆状态信息')
                                if info[-4:-2] == '00':
                                    print('车辆已解锁')
                                    VIN = Converter().to_ascii(info[8:42])
                                    r.zadd('car_status', {VIN: 2})
                                if info[-4:-2] == '01':
                                    print('车辆已锁车')
                                    VIN = Converter().to_ascii(info[8:42])
                                    r.zadd('car_status', {VIN: 1})
                            elif info[62:64] == '07':
                                print('远程升级命令')
                                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475', db='cm',
                                                     charset='utf8')
                                cursor = db.cursor()
                                VIN = Converter().to_ascii(info[8:42])
                                sql = 'select * from car where VIN = "%s";' % VIN
                                cursor.execute(sql)
                                car = cursor.fetchone()
                                cursor.close()
                                db.close()
                                car_ID = car[0]
                                ter_time = Convertertime().to_time(info[48:60])
                                type = 80
                                messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                                ftp = car[10]
                                pwd = car[11]
                                ip = str(car[9]).split('/')[0].split('.')
                                port = '21'
                                ID = 'CPS'
                                ter = '123456'
                                version = car[6]
                                url = car[9]
                                if info[46:48] == '14':
                                    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                         db='cm',
                                                         charset='utf8')
                                    cursor = db.cursor()
                                    query = "update car set status_code = %d where id = %d;" % (int(info[-4:-2], 16), car[0])
                                    print(query)
                                    cursor.execute(query)
                                    db.commit()
                                    cursor.close()
                                    db.close()
                                if version:
                                    ip_hex = '0000'
                                    for item in ip:
                                        ip_hex += hex(int(item))[2:]
                                    if int(version) > int(info[76:86]):
                                        data = Convertertime().to_hex_time() + '01' + Converter().to_hex('mas;' + str(ftp) + ';' + str(pwd) + ';') + ip_hex + '3B' + '00153B' + Converter().to_hex(str(ID) + ';' + str(ter) + ';' + str(version) + ';' + 'ftp://' + str(url) + ';') + '0000'
                                        print(data, 1)
                                        len_data = hex(int(len(data)))[2:]
                                        print(len_data, 2)
                                        if len(len_data) == 1:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + '000' + str(len_data) + data
                                        if len(len_data) == 2:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + '00' + str(len_data) + data
                                        if len(len_data) == 3:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + '0' + str(len_data) + data
                                        if len(len_data) == 4:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + str(len_data) + data
                                        is_bcc = BCC_all(datas)
                                        self.cclient.send(str(Converter().to_ascii(datas + is_bcc)).encode('raw_unicode_escape'))
                                        print('开始升级')
                                        print(datas + is_bcc, 3)
                                        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                             db='cm',
                                                             charset='utf8')
                                        cursor = db.cursor()
                                        query = "update car set status = 1 where id = %d;" % car[0]
                                        print(query)
                                        cursor.execute(query)
                                        db.commit()
                                        cursor.close()
                                        db.close()
                                        continue
                                    elif int(version) == int(info[76:86]):
                                        print('升级完成')
                                        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                             db='cm',
                                                             charset='utf8')
                                        cursor = db.cursor()
                                        query = "update car set status = 2 where id = %d;" % car[0]
                                        print(query)
                                        cursor.execute(query)
                                        db.commit()
                                        query = "update car set version_now = %s, create_time = '%s' where id = %d;" % (info[76:86], ter_time, car[0])
                                        cursor.execute(query)
                                        db.commit()
                                        cursor.close()
                                        db.close()
                                        data = Convertertime().to_hex_time() + '01' + Converter().to_hex(
                                            ';' + str(ftp) + ';' + str(pwd) + ';' + str(ip) + ';' + str(
                                                port) + ';' + str(ID) + ';' + str(ter) + ';' + str(version) + ';' + str(
                                                url) + ';') + '0000'
                                        len_data = hex(int(len(data)))[2:]
                                        if len(len_data) == 1:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + '000' + str(len_data) + data
                                        if len(len_data) == 2:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + '00' + str(len_data) + data
                                        if len(len_data) == 3:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + '0' + str(len_data) + data
                                        if len(len_data) == 4:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + str(len_data) + data
                                        is_bcc = BCC_all(datas)
                                        self.cclient.send(str(Converter().to_ascii(datas + is_bcc)).encode('raw_unicode_escape'))
                                        continue
                                    else:
                                        print('当前版本大于需要升级版本')
                                        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                             db='cm',
                                                             charset='utf8')
                                        cursor = db.cursor()
                                        query = "update car set status = 3 where id = %d;" % car[0]
                                        print(query)
                                        cursor.execute(query)
                                        db.commit()
                                        query = "update car set version_now = %s, create_time = '%s' where id = %d;" % (info[76:86], ter_time, car[0])
                                        cursor.execute(query)
                                        db.commit()
                                        cursor.close()
                                        db.close()
                                        data = Convertertime().to_hex_time() + '01' + Converter().to_hex(';' + str(ftp) + ';' + str(pwd) + ';' + str(ip) + ';' + str(port) + ';' + str(ID) + ';' + str(ter) + ';' + str(version) + ';' + str(url) + ';') + '0000'
                                        len_data = hex(int(len(data)))[2:]
                                        if len(len_data) == 1:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + '000' + str(len_data) + data
                                        if len(len_data) == 2:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + '00' + str(len_data) + data
                                        if len(len_data) == 3:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + '0' + str(len_data) + data
                                        if len(len_data) == 4:
                                            datas = info[:4] + '82fe' + info[8:42] + '01' + str(len_data) + data
                                        is_bcc = BCC_all(datas)
                                        self.cclient.send(str(Converter().to_ascii(datas + is_bcc)).encode('raw_unicode_escape'))
                                        continue
                                else:
                                    print('无版本信息')
                                    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                         db='cm',
                                                         charset='utf8')
                                    cursor = db.cursor()
                                    query = "update car set status = 0 where id = %d;" % car[0]
                                    print(query)
                                    cursor.execute(query)
                                    db.commit()
                                    query = "update car set version_now = %s, create_time = '%s' where id = %d;" % (info[76:86], ter_time, car[0])
                                    print(query)
                                    cursor.execute(query)
                                    db.commit()
                                    cursor.close()
                                    db.close()
                                    data = Convertertime().to_hex_time() + '01' + Converter().to_hex(';' + str(ftp) + ';' + str(pwd) + ';' + str(
                                        ip) + ';' + str(port) + ';' + str(ID) + ';' + str(ter) + ';' + str(version) + ';' + str(
                                        url) + ';') + '0000'
                                    len_data = hex(int(len(data)))[2:]
                                    if len(len_data) == 1:
                                        datas = info[:4] + '82fe' + info[8:42] + '01' + '000' + str(len_data) + data
                                    if len(len_data) == 2:
                                        datas = info[:4] + '82fe' + info[8:42] + '01' + '00' + str(len_data) + data
                                    if len(len_data) == 3:
                                        datas = info[:4] + '82fe' + info[8:42] + '01' + '0' + str(len_data) + data
                                    if len(len_data) == 4:
                                        datas = info[:4] + '82fe' + info[8:42] + '01' + str(len_data) + data
                                    is_bcc = BCC_all(datas)
                                    self.cclient.send(str(Converter().to_ascii(datas + is_bcc)).encode('raw_unicode_escape'))
                                    continue
                            continue
                        if message[4:6] == '82':
                            print('解锁车接收成功')
                            len_data = int(message[44:48], 16)
                            info = message[:48 + len_data * 2 + 2]
                            message = message.replace(info, '', 1)
                            if BCC(info) != info[-2:]:
                                print(info)
                                print('BCC校验失败')
                                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                     db='cm',
                                                     charset='utf8')
                                cursor = db.cursor()
                                VIN = Converter().to_ascii(info[8:42])
                                sql = 'select * from car where VIN = "%s";' % VIN
                                cursor.execute(sql)
                                car = cursor.fetchone()
                                cursor.close()
                                db.close()
                                car_ID = car[0]
                                ter_time = Convertertime().to_time(info[48:60])
                                type = 1002
                                messages['CAN'].append((car_ID, create_time, ter_time, info, type))
                                data = info[:6] + '02' + info[8:42] + '010006' + Convertertime().to_hex_time()
                                my_bcc = BCC_all(data)
                                self.cclient.send(str(Converter().to_ascii(data + my_bcc)).encode('raw_unicode_escape'))
                                message = ''
                                break
                            if info[-4:-2] == '90':
                                VIN = Converter().to_ascii(info[8:42])
                                r.zadd('car', {VIN: 3})
                            continue
                        else:
                            print('无当前功能')
                            message = ''
                print('关闭连接')
                self.cclient.close()
            except socket.timeout:
                print('连接超时,last_message:', last_message)
                try:
                    VIN = Converter().to_ascii(last_message[8:42])
                    r.zrem("car_login", VIN)
                    location = r.geopos('car_online', VIN)
                    r.zrem("car_online", VIN)
                    r.geoadd('car_offline', location[0][0], location[0][1], VIN)
                except:
                    print('车辆超时离线出错')
                    self.cclient.close()
                self.cclient.close()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 2000))
    # sock.bind(('127.0.0.1', 2000))
    # sock.bind(('0.0.0.0', 889))
    # sock.bind(('0.0.0.0', 889))
    # sock.bind(('0.0.0.0', 890))
    sock.listen(5000)

    while True:
        client, address = sock.accept()
        CarTransHandle(client).start()


def set_time():
    """
    设置定时批量插入
    :return:
    """
    try:
        if messages['CAN']:
            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475', db='cm', charset='utf8')
            cursor = db.cursor()
            sql = "INSERT INTO can(car_id, create_time, ter_time, data, type) VALUES (%s,%s,%s,%s,%s)"
            try:
                cursor.executemany(sql, messages['CAN'])
                db.commit()
                messages['CAN'] = []
            except:
                db.rollback()
            cursor.close()
            db.close()

        # 车辆离线存储
        # if messages['offline']:
        #     for item in messages['offline']:
        #         location = r.geopos('car_online', item)
        #         r.zrem("car_online", item)
        #         r.geoadd('car_offline', location[0][0], location[0][1], item)
        #     messages['offline'] = []

        # 车辆在线存储
        if messages['online']:
            for item in messages['online']:
                r.zrem("car_offline", item[2])
                r.geoadd("car_online", item[0], item[1], item[2])
            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475', db='cm', charset='utf8')
            cursor = db.cursor()
            sql = "INSERT INTO back(longitude, latitude, VIN, create_time) VALUES (%s,%s,%s,%s)"
            try:
                cursor.executemany(sql, messages['online'])
                db.commit()
            except:
                db.rollback()
            cursor.close()
            db.close()
            messages['online'] = []

        # 报警车辆存储
        if messages['warning']:
            for item in messages['warning']:
                location = r.geopos('car_online', item)
                r.geoadd('car_warning', location[0][0], location[0][1], item)
        # 报警车辆恢复
        if messages['unwarning']:
            for item in messages['unwarning']:
                r.zrem('car_warning', item)
        Timer(10, set_time).start()
    except:
        print('存储数据出错')
        messages['CAN'] = []
        messages['online'] = []
        # messages['offline'] = []
        messages['warning'] = []
        messages['unwarning'] = []
        Timer(10, set_time).start()

if __name__ == '__main__':
    messages = {}
    messages['CAN'] = []
    messages['online'] = []
    # messages['offline'] = []
    messages['warning'] = []
    messages['unwarning'] = []
    r = redis.Redis(host='localhost', port=6379)
    set_time()
    main()

