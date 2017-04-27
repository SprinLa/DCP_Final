import threading
from Test1 import execute
from Test2 import execute1


def deploy():
    collect_interval = 3
    falcon_interval = 2
    thread_num = 1
    t1 = threading.Thread(target=execute1, args=(collect_interval, thread_num))
    t2 = threading.Thread(target=execute, args=(falcon_interval,))
    # start thread
    t1.start()
    t2.start()

if __name__=='__main__':
    deploy()
