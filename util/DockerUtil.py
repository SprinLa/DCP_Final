import docker
from docker.types.networks import IPAMPool, IPAMConfig
import logging
import os

LOG_FILE_PATH = '/data0/log/DCP.log'

os.system("mkdir -p /data0/log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')

client = docker.APIClient(base_url='unix://var/run/docker.sock')
high_client = docker.from_env()


# create network
def createNetwork(name, subnet, gateway):
    ipam_pool = IPAMPool(subnet=subnet, gateway=gateway)
    ipam_config = IPAMConfig(pool_configs=[ipam_pool])
    result = client.create_network(name, driver="bridge", ipam=ipam_config)
    logging.info(result)
    return result


# create containers create_container
def createContainers(image, name, ports=None, host_config=None, mem_limit=None, networking_config=None):
    container_id = client.create_container(image=image, ports=ports, host_config=host_config, name=name,
                                           mem_limit=mem_limit, detach=True, stdin_open=True, tty=True,
                                           networking_config=networking_config)
    logging.info("create container " + name + " : " + container_id['Id'])
    os.system("docker start " + container_id['Id'])
    return container_id


# createNetwork("test")
def getImages():
    return client.images()


def getContainerStat(name):
    return client.stats(name, False)


# get All containers
def getAllContainers():
    return client.containers()


# get All containers name
def getAllContainersName():
    container_list = getAllContainers()
    container_name_list = []
    for container in container_list:
        container_name_list.append(container['container_name'])
    return container_name_list


def get_host_config(mem_limit=None, ports=None, binds=None):
    # ports is a dict
    host_config = client.create_host_config(mem_limit=mem_limit, port_bindings=ports, binds=binds)
    return host_config


def get_network_config(network_name, ipv4_address):
    networking_config = client.create_networking_config(
        {network_name: client.create_endpoint_config(ipv4_address=ipv4_address)})
    return networking_config


def remove_container(container_name):
    return client.remove_container(container=container_name, force=True)


def restart_container(container_name):
    return client.restart(container=container_name)


class Container_status(object):
    name = ""
    mem_usage_percent = float(0)
    cpu_usage_percent = float(0)
    ip = ""

    def __init__(self, container_name, mem, cpu, ip):
        self.name = container_name
        self.mem_usage_percent = mem
        self.cpu_usage_percent = cpu
        self.ip = ip

    def __repr__(self):
        return 'Name : %s ,cpu_usage : %s,mem_usage : %s,ip is : %s' % (
            self.name, self.cpu_usage_percent, self.mem_usage_percent, self.ip)


if __name__ == '__main__':
    # logging.info("DockerUtil")
    print getContainerStat('fcf9fcec93c1')
    print getAllContainers()
