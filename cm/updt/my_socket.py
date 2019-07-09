import socket

# 建立一个最简单的服务器


def start_ws():
    # 创建一个socket服务端对象
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 监听8000端口
    sock.bind(('localhost', 2001))
    # 最多排队5个
    sock.listen(5)

    while True:
        client, address = sock.accept()
        # 处理请求
        client.recv(1024)
        client.send('HTTP/1.1 200 ok\r\n\r\n'.encode())
        client.send('Hello, This is Webservice'.encode())
        client.close()

start_ws()