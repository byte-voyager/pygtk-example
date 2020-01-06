import setproctitle
from subprocess import Popen
import time
import os
print('start')
print(os.getpid())
res = os.fork()

if res == 0:
    # 子进程执行完 父进程没有正确的获取子进程的退出状态 那么会导致子进程变为僵尸状态
    setproctitle.setproctitle("我是子进程")
    print('我是子进程', os.getpid())
else:
    setproctitle.setproctitle("我是父进程")
    print('我是父进程', os.getpid())
    while 1:
        time.sleep(1)
        print()
