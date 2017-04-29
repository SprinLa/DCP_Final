import logging
import os
import threading
from util.ConfigUtil import Properties
from StatsCollect import executeCollect
from StatsFalcon import executeFalcon

LOG_FILE_PATH = '/data0/log/DCP.log'

os.system("mkdir -p /data0/log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')


def deploy():
    deploy_conf = Properties("../conf/dcp_deploy.conf").getProperties()

    collect_interval = int(deploy_conf['es.collect.interval'])
    falcon_interval = int(deploy_conf['es.falcon.interval'])
    thread_num = int(deploy_conf['es.collect.threadNum'])
    logging.info("start")
    t1 = threading.Thread(target=executeCollect, args=(collect_interval, thread_num))
    t2 = threading.Thread(target=executeFalcon, args=(falcon_interval,))
    # start thread
    t1.start()
    t2.start()


if __name__ == '__main__':
    deploy()
