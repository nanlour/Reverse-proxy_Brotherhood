from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue
from threading import Thread


def echo_handler_s(address, client_sock, queue_s, queue_c):
    print('Got connection from {}'.format(address))

    def c_s(queue_s, client_sock):
        msg_s = queue_s.get()
        client_sock.sendall(msg_s)

    t = Thread(target=c_s, args=(queue_s, client_sock))
    t.start()
    while True:
        msg_c = client_sock.recv(8192)
        queue_c.put(msg_c)
        print(msg_c)
        if not msg_c:
            return 0

    # client_sock.close()


def echo_handler_c(address, client_sock, queue_s, queue_c):
    print('Got connection from {}'.format(address))

    def s_c(queue_c, client_sock):
        msg_c = queue_c.get()
        client_sock.sendall(msg_c)

    t = Thread(target=s_c, args=(queue_c, client_sock))
    t.start()
    while True:
        msg_s = client_sock.recv(8192)
        queue_s.put(msg_s)
        print(msg_s)
        if not msg_s:
            return 0
    # client_sock.close()


def echo_server(address, queue_s, queue_c, s_c, backlog=5):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(backlog)
    while True:
        client_sock, client_addr = sock.accept()
        if s_c:
            echo_handler_s(client_addr, client_sock, queue_s, queue_c)
        else:
            echo_handler_c(client_addr, client_sock, queue_s, queue_c)
        print(s_c + 10)


if __name__ == '__main__':
    q_s, q_c = Queue(), Queue()
    t1 = Thread(target=echo_server, args=(('', 8000), q_s, q_c, 1))
    t2 = Thread(target=echo_server, args=(('', 8888), q_s, q_c, 0))
    t1.start()
    t2.start()
