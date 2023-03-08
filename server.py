from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue
from threading import Thread

LOCALHOST = 'localhost'
VPS = '192.168.217.93'


def echo_handler_s(client_sock, queue_s, queue_c):

    def c_s(queue_s, client_sock):
        while True:
            msg_s = queue_s.get()
            print(2, msg_s)
            client_sock.sendall(msg_s)
            print(2)

    t = Thread(target=c_s, args=(queue_s, client_sock))
    t.start()
    while True:
        msg_c = client_sock.recv(8192)
        print(1, msg_c)
        if not msg_c:
            return 0
        queue_c.put(msg_c)
    # client_sock.close()


def echo_handler_c(client_sock, queue_s, queue_c):

    def s_c(queue_c, client_sock):
        while True:
            msg_c = queue_c.get()
            print(4, msg_c)
            client_sock.sendall(msg_c)
            print(4)

    t = Thread(target=s_c, args=(queue_c, client_sock))
    t.start()
    while True:
        msg_s = client_sock.recv(8192)
        if not msg_s:
            return 0
        queue_s.put(msg_s)
        print(msg_s)
    # client_sock.close()


def echo_server(address, queue_s, queue_c, s_c):
    client_sock = socket(AF_INET, SOCK_STREAM)
    client_sock.connect(address)
    while True:
        if s_c:
            echo_handler_s(client_sock, queue_s, queue_c)
        else:
            echo_handler_c(client_sock, queue_s, queue_c)


if __name__ == '__main__':
    q_s, q_c = Queue(), Queue()
    t1 = Thread(target=echo_server, args=((VPS, 8000), q_s, q_c, 1))
    t2 = Thread(target=echo_server, args=((LOCALHOST, 22), q_s, q_c, 0))
    t1.start()
    t2.start()
