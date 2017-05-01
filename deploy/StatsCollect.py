import os
import threadpool
import logging
from datetime import datetime
from time import sleep
from util.ESUtil import write2es
from util.DockerUtil import getAllContainersName, getContainersNameFromDB, getContainerStat

LOG_FILE_PATH = '/data0/log/DCP.log'

os.system("mkdir -p /data0/log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')

DCP_DB_PATH = "dcp_container"
DCP_ES_PATH = "dcp_es"


def collect_container_stats(name):
    container_stats = getContainerStat(name)
    # CPU
    cpu_total_usage = container_stats['cpu_stats']['cpu_usage']['total_usage']
    cpu_system_uasge = container_stats['cpu_stats']['system_cpu_usage']
    cpu_percent = round((float(cpu_total_usage) / float(cpu_system_uasge)) * 100.0, 2)
    cpu_usage_in_usermod = container_stats['cpu_stats']['cpu_usage']['usage_in_usermode']
    cpu_usage_in_kernelmode = container_stats['cpu_stats']['cpu_usage']['usage_in_kernelmode']
    # Memory
    mem_usage = container_stats['memory_stats']['usage']
    mem_limit = container_stats['memory_stats']['limit']
    mem_swap = container_stats["memory_stats"]["stats"]["swap"]
    mem_percent = round(float(mem_usage) / float(mem_limit) * 100.0, 2)
    # NetWork
    network_rx_packets = container_stats['networks']['eth0']['rx_packets']
    network_tx_packets = container_stats['networks']['eth0']['tx_packets']
    network_rx_bytes = container_stats['networks']['eth0']['rx_bytes']
    network_tx_bytes = container_stats['networks']['eth0']['tx_bytes']  # persecond ?liuliang
    # StateTime
    invoke_time = container_stats['read']
    # pids
    pid_nums = container_stats["pids_stats"]
    # collect_time=str(new_result['read'].split('.')[0].split('T')[0])+' '+str(new_result['read'].split('.')[0].split('T')[1])
    msg = {
        'container_name': name,
        'cpu_percent': cpu_percent,
        'cpu_usage_in_usermod': cpu_usage_in_usermod,
        'cpu_usage_in_kernelmod': cpu_usage_in_kernelmode,
        'memory_usage': mem_usage,
        'memory_limit': mem_limit,
        'memory_percent': mem_percent,
        'memory_swap': mem_swap,
        # 'memory_percent': mem_percent,
        'network_rx_packets': network_rx_packets,
        'network_tx_packets': network_tx_packets,
        'network_rx_bytes': network_rx_bytes,
        'network_tx_bytes': network_tx_bytes,
        'invoke_time': invoke_time,
        'pid_nums': pid_nums
    }
    logging.info(msg)

    send2es(msg)


def send2es(msg):
    cal_time = datetime.now()

    container_name = msg['container_name']

    container_ip = os.popen("docker inspect --format '{{ .NetworkSettings.IPAddress }}' " + container_name).read()

    msg['cal_time'] = cal_time

    msg['container_ip'] = container_ip

    # write2es("docker-index", "test2", body=msg)

    logging.info("write2es " + container_name + " stats success")


def executeCollect(interval, thread_num):
    pool = threadpool.ThreadPool(thread_num)

    while True:
        # container_name_list = getAllContainersName()
        container_name_list = getContainersNameFromDB(DCP_DB_PATH)
        container_name_list += getContainersNameFromDB(DCP_ES_PATH)

        requests = threadpool.makeRequests(collect_container_stats, container_name_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        sleep(interval / 1000)


if __name__ == '__main__':
    # while True:
    #     executeCollect(1000, 10)
    for container_name in getAllContainersName():
        print getContainerStat(container_name)
    container_name_list = getContainersNameFromDB(DCP_DB_PATH)
    container_name_list += getContainersNameFromDB(DCP_ES_PATH)
    print container_name_list
