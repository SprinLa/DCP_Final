import os
import logging
from DBUtil import selectByKey
import time

NGINX_PATH = "/usr/local/nginx"

LOG_FILE_PATH = '/data0/log/DCP.log'

NGINX_CONFIG_PATH = NGINX_PATH + "/conf/nginx.conf"
NGINX_SBIN_PATH = NGINX_PATH + "/sbin"

os.system("mkdir -p /data0/log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')
DCP_CONF_DB = "dcp_conf"


def nginx_reload(config):
    logging.info("nginx reload ...")
    subnet = selectByKey(DCP_CONF_DB, "app_start_network")

    server_list = os.popen("cat " + NGINX_CONFIG_PATH + " | grep  \"server " + subnet + "\"").read()

    conf_file = open(NGINX_CONFIG_PATH, 'r')
    all_lines = conf_file.read()
    if len(server_list) == 0:
        new_lines = all_lines.replace("upstream localhost{", "upstream localhost{" + "\n" + config)
    else:
        server_list = server_list[0:len(server_list) - 1]
        server_list_configure = config
        new_lines = all_lines.replace(server_list, server_list_configure)
    logging.info("new host list:" + new_lines)
    # conf_file.write(all_lines)
    conf_file.close()
    conf_file_write = open(NGINX_CONFIG_PATH, "w")
    conf_file_write.write(new_lines)

    time.sleep(1)


def get_nginx_config(container_dict):
    container_port = "80"
    config = ""
    for container_name in container_dict.keys():
        conf = "server " + container_dict[container_name] + ":" + container_port + ";" + "\n"
        config += conf
    logging.info("current config : " + config)
    return config


def stop_nginx():
    status = os.system(NGINX_SBIN_PATH + "/" + "nginx -s quit")

    if status == 0:
        logging.info("nginx stop success")
    else:
        logging.error("nginx stop failed")
