"""
file: service.py
socket service
"""

import socket
import threading
import time
import sys

clients = {}


class Client:
    def __init__(self, conn, msg_str):
        self.desc = self.get_desc(conn)
        msg = msg_str.split(',')
        self.x = msg[1]
        self.y = msg[2]
        self.z = msg[3]

    @staticmethod
    def get_desc(conn):
        return f'{conn.getpeername()[0]}:{conn.getpeername()[1]}'

    def get_position(self):
        return f'{self.desc},{self.x},{self.y},{self.z}'

    def move(self, msg_str):
        msg = msg_str.split(',')
        (x, y, z) = (msg[1], msg[2], msg[3])
        return f'{self.desc},{x},{y},{z}'

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
        # conns.append(conn)
        threading.Thread(target=deal_data, args=(conn, addr)).start()


def handle_move(conn, msg):
    client = clients[conn]
    send(f'Move|{client.move(msg)}')


def handle_enter(conn, msg):
    new_client = Client(conn, msg)
    send('Enter|' + new_client.get_position())
    clients[conn] = new_client


def handle_list(conn):
    msg = 'List|'
    for conn, client in clients.items():
        msg += client.get_position() + ','
    conn_send(conn, msg)


def handle_leave(conn):
    msg = f"Leave|{Client.get_desc(conn)}"
    send(msg)


def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))

    while True:
        data = conn.recv(1024)
        print(f'Recv message: {data.decode("utf-8")}')
        if len(data) != 0:
            message = data.decode('utf-8').split('|')
            event = message[0]
            msg = message[1]
            if event == 'Enter':
                handle_enter(conn, msg)
            elif event == "List":
                handle_list(conn)
            elif event == "Move":
                handle_move(conn, msg)
        else:
            if conn in clients.keys():
                address_port = conn.getpeername()
                print(f"客户端掉线：{address_port[0]}:{address_port[1]}")
                handle_leave(conn)
                del (clients[conn])
            else:
                conn.close()


def conn_send(conn, message):
    print(message)
    conn.send(message.encode('utf-8'))


def send(message):
    print(message)
    for conn in clients:
        conn.send(message.encode('utf-8'))


if __name__ == '__main__':
    socket_service()
