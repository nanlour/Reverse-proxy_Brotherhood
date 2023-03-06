import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue

VPS = '127.0.0.1'


def client():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((VPS, 8000))
    while True:
        s.send(b'im wr133')
        print(s.recv(8192))
        time.sleep(2)


for n in range(10):
    t = Thread(target=client)
    t.start()
