import os
import sys
import datetime
import socket
import signal

signal.signal(signal.SIGTERM, signal.SIG_DFL)

"""
无名管道利用父子进程能够复制相同文件描述父的机制
命名管道可以在没有血缘关系的两个进程之间通信
dup可以复制文件描述符 返回最小可用的
dup2 可以指定复制哪个
sendfile 可以在socket文件描述符号和文件描述父进行文件0拷贝
"""

def main():
    fd = os.open('./a.txt', os.O_CREAT | os.O_RDWR)
    backup = os.dup(fd)
    replaced = os.dup2(fd, sys.stdout.fileno())
    # os.dup2(sys.stdout.fileno(), fd)
    # print(sys.stderr.fileno())
    # os.close(fd)
    print('sdsdsd')
    # os.close(fd)


def main2():
    fd = os.open('./a2.txt', os.O_CREAT | os.O_RDWR | os.O_APPEND)
    # new_out = os.dup(sys.stdout.fileno())
    print(sys.stdout.fileno())
    os.dup2(fd, 1)

    print(datetime.datetime.now(), 'hello world!')


def main3():
    fd = os.open('./a3.txt', os.O_CREAT | os.O_RDWR | os.O_APPEND)
    os.close(1)
    os.dup(fd)
    print(datetime.datetime.now(), '我会输出到文件')


def main4():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 9009))
    server.listen()
    while 1:
        print('waiting connection...')
        client, addr = server.accept()
        print('new connection:', client, addr)
        data = client.recv(1024)
        print(data)
        fd = os.open('./a3.txt', os.O_CREAT | os.O_RDWR | os.O_APPEND)
        stat = os.fstat(fd)
        print('文件大小', stat.st_size, "fd", fd)
        os.sendfile(client.fileno(), fd, None, stat.st_size)
        os.fstat(fd)
        os.close(fd)  # 如果不关掉导致文件描述符递增
        client.close()


def main5():
    fd = os.open('./a3.txt', os.O_CREAT | os.O_RDWR | os.O_APPEND)
    stat = os.fstat(fd)
    print(stat)
    os.close(fd)

if __name__ == '__main__':
    main4()
