import socket

import time

import redis


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
        client.connect(('127.0.0.1', 2000))
        while True:
                data = '232301fe54424f584333324130303030303030303101007e1309090f2731000538393836303433393130313838303238333331340160000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d3'
                client.send(str(Converter().to_ascii(data)).encode('raw_unicode_escape'))
                me = Converter().to_hex(client.recv(2048).decode('raw_unicode_escape'))
                print(me)
                time.sleep(1000)

if __name__ == '__main__':
    # main()
        info = '232301fe4c44503532413936354a4e343237353434010025130a1c12190a00023839323434303230303030383434363835333137010700000000000000f8'
        print(info[64:104])