import socket
from threading import Thread, Timer
import datetime
import pymysql
import redis
import time


def main():
    def BCC(q):
        """
        BCC异或校验法
        :param q:
        :return: 16进制数
        """
        sum = 0
        for i in range(2, len(q), 2):
            sum = int(hex(sum ^ int(q[i-2:i], 16)), 16)
        return hex(sum)[2:]

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
            list_h = []
            for c in s:
                list_h.append(str(hex(ord(c))[2:]))
            return ''.join(list_h)

    class CarTransHandle(Thread):
        """
        自定义线程类
        """
        def __init__(self, cclient):
            super().__init__()
            self.cclient = cclient

        def run(self):
            while True:
                message = self.cclient.recv(2048).decode('utf-8')
                print(message)
                if not message:
                    print('tcp连接中断')
                    try:
                        messages['offline'].append(Converter().to_ascii(last_message[8:42]))
                        break
                    except:
                        pass
                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475', db='cm',
                                     charset='utf8')
                cursor = db.cursor()
                VIN = Converter().to_ascii(message[8:42])
                sql = 'select * from car where VIN = "%s";' % VIN
                cursor.execute(sql)
                car = cursor.fetchone()
                cursor.close()
                db.close()
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ter_time = Convertertime().to_time(message[48:60])
                if BCC(message) != message[-2:]:
                    print('BCC校验失败')
                    car_ID = car[0]
                    type = 1002
                    messages['CAN'].append((car_ID, create_time, ter_time, message, type))
                    data = message[:6] + '02' + message[8:42] + '010006' + Convertertime().to_hex_time()
                    my_bcc = BCC(data)
                    self.cclient.send(str(data + my_bcc).encode('utf-8'))
                    break
                if message[4:6] == '01':
                    print('车辆登入')
                    car_ID = car[0]
                    type = 1
                    messages['CAN'].append((car_ID, create_time, ter_time, message, type))
                    if not car:
                        type = 1003
                        messages['CAN'].append((car_ID, create_time, ter_time, message, type))
                        data = message[:6] + '02' + message[8:42] + '010006' + Convertertime().to_hex_time()
                        my_bcc = BCC(data)
                        self.cclient.send(str(data + my_bcc).encode('utf-8'))
                        print('车辆登录失败')
                        break
                    data = message[:6] + '01' + message[8:42] + '010006' + Convertertime().to_hex_time()
                    my_bcc = BCC(data)
                    self.cclient.send(str(data + my_bcc).encode('utf-8'))
                if message[4:6] == '02':
                    print('实时信息上报')
                    car_ID = car[0]
                    type = 2
                    messages['CAN'].append((car_ID, create_time, ter_time, message, type))
                    data = message[60:-2]
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
                                    messages['online'].append((longitude, latitude, VIN))
                                data = data.replace(data[0:20], '', 1)
                            if data[0:2] == '06':
                                data = data.replace(data[0:30], '', 1)
                            if data[0:2] == '07':
                                if data[2:4] != '00':
                                    print('车辆报警')
                                    messages['warning'].append(VIN)
                                else:
                                    messages['unwarning'].append(VIN)
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
                    except:
                        print('上报信息错误')
                        type = 1001
                        messages['CAN'].append((car_ID, create_time, ter_time, message, type))

                if message[4:6] == '03':
                    print('补发信息上报')
                    car_ID = car[0]
                    type = 3
                    messages['CAN'].append((car_ID, create_time, ter_time, message, type))
                    data = message[60:-2]
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
                                    messages['online'].append((longitude, latitude, VIN))
                                data = data.replace(data[0:20], '', 1)
                            if data[0:2] == '06':
                                data = data.replace(data[0:30], '', 1)
                            if data[0:2] == '07':
                                if data[2:4] != '00':
                                    print('车辆报警')
                                    messages['warning'].append(VIN)
                                messages['unwarning'].append(VIN)
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
                    except:
                        print('上报信息错误')
                        type = 1001
                        messages['CAN'].append((car_ID, create_time, ter_time, message, type))

                if message[4:6] == '04':
                    print('车辆登出')
                    car_ID = car[0]
                    type = 4
                    messages['CAN'].append((car_ID, create_time, ter_time, message, type))
                    messages['offline'].append(VIN)
                    break
                if message[4:6] == '07':
                    print('心跳')
                    data = message[:6] + '01' + message[8:42] + '010006' + Convertertime().to_hex_time()
                    my_bcc = BCC(data)
                    self.cclient.send(str(data + my_bcc).encode('utf-8'))
                if message[4:6] == '80':
                    car_ID = car[0]
                    type = 80
                    messages['CAN'].append((car_ID, create_time, ter_time, message, type))
                    print('远程升级命令')
                    ftp = car[9]
                    pwd = car[10]
                    ip = str(car[8]).split('/')[0]
                    port = '21'
                    ID = 'CPS'
                    ter = '123456'
                    version = car[6]
                    url = car[8]
                    if message[-4:-2] == '68' or message[-4:-2] == '64' or message[-4:-2] == '00':
                        if int(version) > int(message[76:86]):
                            data = Convertertime().to_hex_time() + '01' + Converter().to_hex('mas;' + ftp + ';' + pwd + ';' + ip + ';' + port + ';' + ID + ';' + ter + ';' + version + ';' + url + ';') + '0000'
                            len_data = hex(int(len(data)/2))[2:]
                            if len(len_data) == 1:
                                datas = message[:4] + '82fe' + message[8:42] + '01' + '000' + str(len_data) + data
                            if len(len_data) == 2:
                                datas = message[:4] + '82fe' + message[8:42] + '01' + '00' + str(len_data) + data
                            if len(len_data) == 3:
                                datas = message[:4] + '82fe' + message[8:42] + '01' + '0' + str(len_data) + data
                            if len(len_data) == 4:
                                datas = message[:4] + '82fe' + message[8:42] + '01' + str(len_data) + data
                            is_bcc = BCC(datas)
                            self.cclient.send(str(datas + is_bcc).encode('utf-8'))
                        else:
                            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                                 db='cm',
                                                 charset='utf8')
                            cursor = db.cursor()
                            query = "update car set status = 0 where id = %d;" % car[0]
                            print(query)
                            cursor.execute(query)
                            db.commit()
                            cursor.close()
                            db.close()
                            data = Convertertime().to_hex_time() + '01' + Converter().to_hex(';' + ftp + ';' + pwd + ';' + ip + ';' + port + ';' + ID + ';' + ter + ';' + version + ';' + url + ';') + '0000'
                            len_data = hex(int(len(data) / 2))[2:]
                            if len(len_data) == 1:
                                datas = message[:4] + '82fe' + message[8:42] + '01' + '000' + str(len_data) + data
                            if len(len_data) == 2:
                                datas = message[:4] + '82fe' + message[8:42] + '01' + '00' + str(len_data) + data
                            if len(len_data) == 3:
                                datas = message[:4] + '82fe' + message[8:42] + '01' + '0' + str(len_data) + data
                            if len(len_data) == 4:
                                datas = message[:4] + '82fe' + message[8:42] + '01' + str(len_data) + data
                            is_bcc = BCC(datas)
                            self.cclient.send(str(datas + is_bcc).encode('utf-8'))
                    else:
                        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='ruige254475',
                                             db='cm',
                                             charset='utf8')
                        cursor = db.cursor()
                        query = "update car set status = 2 where id = %d;" % car[0]
                        cursor.execute(query)
                        db.commit()
                        cursor.close()
                        db.close()
                        data = Convertertime().to_hex_time() + '01' + Converter().to_hex(
                            'mas;' + ftp + ';' + pwd + ';' + ip + ';' + port + ';' + ID + ';' + ter + ';' + version + ';' + url + ';') + '0000'
                        len_data = hex(int(len(data) / 2))[2:]
                        if len(len_data) == 1:
                            datas = message[:4] + '82fe' + message[8:42] + '01' + '000' + str(len_data) + data
                        if len(len_data) == 2:
                            datas = message[:4] + '82fe' + message[8:42] + '01' + '00' + str(len_data) + data
                        if len(len_data) == 3:
                            datas = message[:4] + '82fe' + message[8:42] + '01' + '0' + str(len_data) + data
                        if len(len_data) == 4:
                            datas = message[:4] + '82fe' + message[8:42] + '01' + str(len_data) + data
                        is_bcc = BCC(datas)
                        self.cclient.send(str(datas + is_bcc).encode('utf-8'))
                last_message = message
            self.cclient.close()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 2000))
    sock.listen(512)

    while True:
        client, address = sock.accept()
        CarTransHandle(client).start()


def set_time():
    """
    设置定时批量插入
    :return:
    """
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
    if messages['offline']:
        r = redis.Redis(host='localhost', port=6379)
        for item in messages['offline']:
            location = r.geopos('car_online', item)
            r.zrem("car_online", item)
            r.geoadd('car_offline', location[0][0], location[0][1], item)
        messages['offline'] = []

    # 车辆在线存储
    if messages['online']:
        r = redis.Redis(host='localhost', port=6379)
        for item in messages['online']:
            r.zrem("car_offline", item[2])
            r.geoadd("car_online", item[0], item[1], item[2])
        messages['online'] = []

    # 报警车辆存储
    if messages['warning']:
        r = redis.Redis(host='localhost', port=6379)
        for item in messages['warning']:
            location = r.geopos('car_online', item)
            r.geoadd('car_warning', location[0][0], location[0][1], item)
    # 报警车辆恢复
    if messages['unwarning']:
        r = redis.Redis(host='localhost', port=6379)
        for item in messages['unwarning']:
            r.zrem('car_warning', item)
    Timer(10, set_time).start()

if __name__ == '__main__':
    messages = {}
    messages['CAN'] = []
    messages['online'] = []
    messages['offline'] = []
    messages['warning'] = []
    messages['unwarning'] = []
    set_time()
    main()

