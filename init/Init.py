import logging
import os
from util.ConfigUtil import Properties
from util.DockerUtil import createContainers, get_host_config, get_network_config
from util.DBUtil import bulk_insert, insert
from util.NginxUtil import get_nginx_config, nginx_reload

LOG_FILE_PATH = '/data0/log/DCP.log'

os.system("mkdir -p /data0/log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')

DCP_DB_PATH = "dcp_container"
DCP_CONF_PATH = "dcp_conf"
ES_DB_PATH = "dcp_es"


def init():
    init_conf = Properties("../conf/dcp_init.conf").getProperties()
    # app_container_dict
    app_container_dict = {}
    es_container_dict = {}
    # read properties
    es_network_name = init_conf['es.network.name']
    es_network_subnet = init_conf['es.network.subnet']
    es_network_gateway = init_conf['es.network.gateway']

    app_network_name = init_conf['app.network.name']
    app_network_subnet = init_conf['app.network.subnet']
    app_network_gateway = init_conf['app.network.gateway']

    app_container_num = int(init_conf['dcp.container.num'])
    app_container_image = init_conf['dcp.image.name']
    app_container_mem = init_conf['dcp.container.mem']

    es_container_num = int(init_conf['es.container.num'])
    es_image_name = init_conf['es.image.name']
    # insert into db app info
    insert(DCP_CONF_PATH, "app_container_image", app_container_image)
    insert(DCP_CONF_PATH, "app_container_mem", app_container_mem)
    insert(DCP_CONF_PATH, "app_network_name", app_network_name)
    # create network !!!!!
    # createNetwork(es_network_name, es_network_subnet, es_network_gateway)
    # createNetwork(app_network_name, app_network_subnet, app_network_gateway)
    # insert into db how many app containers
    insert(DCP_CONF_PATH, "app_container_num", str(app_container_num))
    # get APP containers IPs
    app_start_ip = init_conf['app.network.first']
    app_start_network = ".".join(app_start_ip.split(".")[0:3])
    app_start_host = app_start_ip.split(".")[3]
    # insert into db the ip start
    insert(DCP_CONF_PATH, "app_start_network", app_start_network)
    insert(DCP_CONF_PATH, "app_start_host", app_start_host)
    # create APP containers
    for i in range(0, app_container_num):
        app_container_name = "APP-" + str(i)
        # publish port = 80
        app_host_config = get_host_config(mem_limit=app_container_mem, ports={80: None})
        # ! IPv4 address
        app_ip_address = app_start_network + "." + str(int(app_start_host) + i)
        app_network_config = get_network_config(app_network_name, app_ip_address)

        createContainers(image=app_container_image, name=app_container_name, host_config=app_host_config,
                         networking_config=app_network_config)

        app_container_dict[app_container_name] = app_ip_address
    # get ES_cluster IPs
    es_network_cluster = str(init_conf['es.network.cluster']).split(",")
    # create ES_cluster
    for i in range(0, es_container_num):
        es_container_name = "ES-" + str(i)
        # publish ports 9200/tcp 9300/tcp
        es_host_config = get_host_config(ports={9200: None, 9300: None})
        es_ip_address = es_network_cluster[i]
        es_network_config = get_network_config(es_network_name, es_ip_address)
        createContainers(image=es_image_name, name=es_container_name, host_config=es_host_config,
                         networking_config=es_network_config)

        es_container_dict[es_container_name] = es_ip_address

    bulk_insert(DCP_DB_PATH, app_container_dict)
    bulk_insert(ES_DB_PATH, es_container_dict)
    config = get_nginx_config(app_container_dict)
    nginx_reload(config)

    print init_conf


if __name__ == '__main__':
    init()
