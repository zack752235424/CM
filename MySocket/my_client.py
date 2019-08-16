import socket

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
        client.connect(('127.0.0.1', 2000))
        while True:
                data = '232301fe4c44503532413936354a4e34323735333901000613071f0a0e0fd6'
                client.send(str(Converter().to_ascii(data)).encode('raw_unicode_escape'))
                me = Converter().to_hex(client.recv(2048).decode('raw_unicode_escape'))
                print(me)
                time.sleep(10)

if __name__ == '__main__':
    main()
