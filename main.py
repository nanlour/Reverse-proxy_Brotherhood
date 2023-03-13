import time
from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue
from threading import Thread


def echo_handler(client_sock, client_addr, queue_1, queue_2, queue_q):
    print('Got connection from {}'.format(client_addr))

    def c_s(queue_1, client_sock):
        while True:
            msg_1 = queue_1.get()
            if not queue_q.empty():
                client_sock.close()
                break
            client_sock.sendall(msg_1)

    t = Thread(target=c_s, args=(queue_1, client_sock))
    t.start()
    try:
        while True:
            msg_2 = client_sock.recv(8192)
            # if sock closed by remote server, msg_2 = b''
            queue_2.put(msg_2)
            if not msg_2 or not queue_q.empty():
                queue_q.put(b'')
                break
    except:
        pass
    finally:
        client_sock.close()
        queue_q.put(b'')



def echo_server(address_c, address_s, backlog=5):
    sock_s = socket(AF_INET, SOCK_STREAM)
    sock_s.bind(address_s)
    sock_s.listen(backlog)

    sock_c = socket(AF_INET, SOCK_STREAM)
    sock_c.bind(address_c)
    sock_c.listen(backlog)
    while True:
        try:
            client_sock_c, client_addr_c = sock_c.accept()
            client_sock_s, client_addr_s = sock_s.accept()

            q_s, q_c, q_q = Queue(), Queue(), Queue()

            t1 = Thread(target=echo_handler, args=(client_sock_c, client_addr_c, q_c, q_s, q_q))
            t2 = Thread(target=echo_handler, args=(client_sock_s, client_addr_s, q_s, q_c, q_q))

            t1.start(), t2.start()

            q_q.get(), q_q.put(b'')
            q_s.put(b''), q_c.put(b'')
        except:
            print('finish444444444444444444444444444444444444444444444444444444444444')
            time.sleep(10)



if __name__ == '__main__':
    address_s = ('', 8888)
    address_c = ('', 8000)
    echo_server(address_c, address_s)
