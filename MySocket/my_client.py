import socket

import time


def main():
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 2000))
        # while True:
        client.send(str('232302fe4c44503533413936324b433039353032320100bd13070811112c01010301000000000c0804ea273543010013880000050006afb0a401ea2bf802010103484e204e204604ea2710070000000000010000000800000008010104ea273500260001260cf80cf50cf70cf70cf80cf60cf80cf70cf60cf70cf50cf60cf40cf40cf50cf60cf80cf40cf60cf60cf60cf40cf40cf40cf50cf50cf70cf60cf60cf60cf60cf60cf50cf40cf50cf40cf50cf50901010010434342424242424343434343444343430601010cf8010d0cf4010d44010342cb').encode('utf-8'))
        message = client.recv(1024).decode('utf-8')
        print(message)
if __name__ == '__main__':
    main()
