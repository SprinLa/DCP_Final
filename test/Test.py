import random
from util.ConfigUtil import Properties
from util.DockerUtil import getAllContainers
import threading
import time
import bsddb

# num = random.randint(10, 20)
print "aaa"


def getNum(num):
    time.sleep(5)
    print num


def getNum2(num,a):
    time.sleep(3)
    print 3


if __name__ == '__main__':
    # init_conf = Properties("../conf/dcp_init.conf").getProperties()
    # print str(init_conf['es.network.cluster']).split(",")
    # threads = []
    # t1 = threading.Thread(target=getNum, args=(2,))
    # threads.append(t1)
    # t2 = threading.Thread(target=getNum2, args=(2,3))
    # threads.append(t2)
    # for t in threads:
    #     t.start()
    # time.sleep(2)
    do = []
    print len(do)
    print len("nen")

