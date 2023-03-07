from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue
from threading import Thread


def echo_handler_s(address, client_sock, queue_s, queue_c):
    print('Got connection from {}'.format(address))
    while not queue_c.empty():
        queue_c.get()
    while not queue_s.empty():
        queue_s.get()
    print(1)
    while True:
        msg_s = queue_s.get()
        print(5, msg_s)
        if not msg_s:
            print(6)
            break
        client_sock.sendall(msg_s)
        msg_c = client_sock.recv(8192)
        if not msg_c:
            break
        queue_c.put(msg_c)
    client_sock.close()


def echo_handler_c(address, client_sock, queue_s, queue_c):
    print('Got connection from {}'.format(address))
    print(3)
    while not queue_c.empty():
        queue_c.get()
    while not queue_s.empty():
        queue_s.get()
    print(2)
    while True:
        msg_s = client_sock.recv(8192)
        queue_s.put(msg_s)
        print(4)
        if not msg_s:
            break
        msg_c = queue_c.get()
        if not msg_c:
            break
        client_sock.sendall(msg_c)
    client_sock.close()


def echo_server(address, queue_s, queue_c, s_c, backlog=5):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(backlog)
    while True:
        try:
            client_sock, client_addr = sock.accept()
            if s_c:
                echo_handler_s(client_addr, client_sock, queue_s, queue_c)
            else:
                echo_handler_c(client_addr, client_sock, queue_s, queue_c)
        except:
            pass


if __name__ == '__main__':
    q_s, q_c = Queue(), Queue()
    t1 = Thread(target=echo_server, args=(('', 8000), q_s, q_c, 1))
    t2 = Thread(target=echo_server, args=(('', 8888), q_s, q_c, 0))
    t1.start()
    t2.start()
