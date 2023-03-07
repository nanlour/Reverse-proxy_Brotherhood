import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue

VPS = '127.0.0.1'


def server():
    s_s = socket(AF_INET, SOCK_STREAM)
    s_s.connect(('localhost', 8888))
    s_s.sendall(b'im wr')
    s_s.recv(8192)


server()