"""
file: service.py
socket service
"""

import socket
import threading
import time
import sys

conns = []


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 6666))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')
    while True:
        conn, addr = s.accept()
        conns.append(conn)
        threading.Thread(target=deal_data, args=(conn, addr)).start()


def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))

    while True:
        data = conn.recv(1024)
        if len(data) != 0:
            send(data)
        else:
            if conn in conns:
                print(f"客户端掉线：{conn}")
                conns.remove(conn)


def send(message):
    print(message)
    for conn in conns:
        # conn.sendall('Hi, Welcome to the server!'.encode('utf-8'))
        conn.send(message)


if __name__ == '__main__':
    socket_service()
