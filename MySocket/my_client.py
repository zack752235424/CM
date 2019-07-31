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
        client.connect(('127.0.0.1', 2000))
        num = 0
        # while True:
        data = '232301fe4c44503532413936354a4e34323735333901000613071f0a0e0fd6'
        client.send(str(Converter().to_ascii(data)).encode('raw_unicode_escape'))
        me = Converter().to_hex(client.recv(2048).decode('raw_unicode_escape'))
        print(me)
                # time.sleep(1)
                # num += 1
                # if num == 10:
                #         data = '232302fe4c44503533413936324b4330393530323201012513071e10222401010301000000000c260b4a178d450100000100000501001800090000000002010100524e204e20520b36271007000000000001010000000000000801010b4a178d00580001580cd30cd40cd20cd60cd60cd60cd20cd50cd60cd60cd20cce0cd60cd80cd40cd50cd80cd50cda0cd60cd60cd50cd30cd20cd20cd30cd40cd40cd10cd80cd90cd20cd80cd50ccf0ccf0cd10cd40cd50ccd0cd80cda0cd60cd40cd10cd70cd60ccf0cd30cd90cd40cd80cd20cd20cd40cd20cd20cd40cd20cd60cd60cd30cd50cd80cdb0cd40cd30cd50cd10cd50cd30cd40cd30cd70cd40cd30cd10cd60cd30cd50cd70cd30cd60cda0cd40cd40cd40cd8090101001441414141414141414141414141404141414141410601410cdb01280ccd010141010e40e8'
                #         client.send(str(Converter().to_ascii(data)).encode('raw_unicode_escape'))
                #         num = 0


if __name__ == '__main__':
    main()
