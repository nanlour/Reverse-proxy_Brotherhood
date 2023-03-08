from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue
from threading import Thread

LOCALHOST = 'localhost'
VPS = ''


def echo_handler_s(client_sock, queue_s, queue_c):
    def s_c(queue_c, client_sock):
        msg_c = client_sock.recv(8192)
        queue_c.put(msg_c)

    def c_s(queue_s, client_sock):
        msg_s = queue_s.get()
        client_sock.sendall(msg_s)

    t1 = Thread(target=c_s, args=(queue_s, client_sock))
    t2 = Thread(target=s_c, args=(queue_c, client_sock))
    t1.start()
    t2.start()
    # client_sock.close()


def echo_handler_c(client_sock, queue_s, queue_c):
    def c_s(queue_s, client_sock):
        msg_s = client_sock.recv(8192)
        queue_s.put(msg_s)

    def s_c(queue_c, client_sock):
        msg_c = queue_c.get()
        client_sock.sendall(msg_c)

    t1 = Thread(target=c_s, args=(queue_s, client_sock))
    t2 = Thread(target=s_c, args=(queue_c, client_sock))
    t1.start()
    t2.start()
    # client_sock.close()


def echo_server(address, queue_s, queue_c, s_c):
    client_sock = socket(AF_INET, SOCK_STREAM)
    while True:
        try:
            client_sock.connect(address)
            if s_c:
                echo_handler_s(client_sock, queue_s, queue_c)
            else:
                echo_handler_c(client_sock, queue_s, queue_c)
        except:
            pass


if __name__ == '__main__':
    q_s, q_c = Queue(), Queue()
    t1 = Thread(target=echo_server, args=((VPS, 8000), q_s, q_c, 1))
    t2 = Thread(target=echo_server, args=((LOCALHOST, 22), q_s, q_c, 0))
    t1.start()
    t2.start()
