import time
from socketserver import BaseRequestHandler, TCPServer
from socket import socket, AF_INET, SOCK_STREAM
from socketserver import ThreadingTCPServer
from queue import Queue
from threading import Thread

REMOTE_HOST = '192.168.0.102'


def pf(f, b):
    while True:
        msg = f.recv(8192)
        print(msg)
        if not msg:
            break
        b.send(msg)


class EchoHandler(BaseRequestHandler):

    def handle(self):
        print('Got connection from', self.client_address)
        s = socket(AF_INET, SOCK_STREAM)


if __name__ == '__main__':
    serv = ThreadingTCPServer(('', 8000), EchoHandler)
    serv.serve_forever()

'''if __name__ == '__main__':
    serv = TCPServer(('', 8000), EchoHandler)
    serv.serve_forever()'''
