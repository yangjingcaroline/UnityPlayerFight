import socket
import sys
import threading

def recv_msg(conn):

        data = conn.recv(1024)
        print("recv: " + data.decode('utf-8'))

def send_msg(conn):
    while True:
        data = input('please input work: ').encode('utf-8')
        conn.sendall(data)



def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6666))
        threading.Thread(target=send_msg, args=(s, )).start()
        threading.Thread(target=recv_msg, args=(s,)).start()

    except socket.error as msg:
        print(msg)
        sys.exit(1)
    while 1:
        data = s.recv(1024)
        print("recv: " + data.decode())
        # data = input('please input work: ').encode()
        # s.sendall(data)
        # data = s.recv(1024)
        # print("recv: " + data.decode())
        if data == 'exit':
            break
    s.close()


if __name__ == '__main__':
    socket_client()