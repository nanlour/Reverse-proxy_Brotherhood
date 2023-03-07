import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue

VPS = '127.0.0.1'


def server():
    s_p = socket(AF_INET, SOCK_STREAM)
    s_p.connect((VPS, 8000))
    s_s = socket(AF_INET, SOCK_STREAM)
    s_s.connect(('localhost', 22))
    print(2)
    while True:
        msg_s = s_p.recv(8192)
        print(msg_s)
        s_s.sendall(msg_s)
        msg_p = s_s.recv(8192)
        print(msg_p)
        s_p.sendall(msg_p)


while True:
    try:
        server()
    except:
        print(7)
        pass
