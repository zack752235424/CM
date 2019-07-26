import socket
import binascii

import time


def main():
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

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('39.106.156.137', 2000))
        # while True:
        data = '232308fe544c474633443934324a484c3030303037010000df'
        client.send(str(Converter().to_ascii(data)).encode('raw_unicode_escape'))
        message = Converter().to_hex(client.recv(2048).decode('raw_unicode_escape'))
        print(message)

if __name__ == '__main__':
    main()

    # def BCC(q):
    #     """
    #     BCC异或校验法
    #     :param q:
    #     :return: 16进制数
    #     """
    #     sum = 0
    #     for i in range(2, len(q), 2):
    #         sum = int(hex(sum ^ int(q[i-2:i], 16)), 16)
    #     result = hex(sum)[2:]
    #     if len(result) == 1:
    #         return '0' + result
    #     return result
    # print(BCC('232308fe4c44503533413936324b433039350303232100251307050e2f0500013839383631313138323333303333343533383930010733313431313643b1'))
