import os
import logging

NGINX_PATH = ""

LOG_FILE_PATH = '/data0/log/DCP.log'
NGINX_PATH = ""
NGINX_CONFIG_PATH = ""
NGINX_SBIN_PATH = ""

os.system("mkdir -p /data0/log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')


def nginx_reload(config):
    logging.info("nginx reload ...")
    SUBNET = ""

    server_list = os.popen("cat " + NGINX_PATH + " | grep  \"server " + SUBNET + "\"").read()
    server_list = server_list[0:len(server_list) - 1]
    server_list_configure = config
    conf_file = open(NGINX_PATH, 'r')
    all_lines = conf_file.read()

    new_lines = all_lines.replace(server_list, server_list_configure)
    logging.info("new host list:" + new_lines)
    # conf_file.write(all_lines)
    conf_file.close()
    conf_file_write = open(NGINX_PATH, "w")
    conf_file_write.write(new_lines)

    command = NGINX_PATH + " -s reload"
    status = os.system(command)

    if status == 0:
        print "nginx reload success"
    else:
        print "nginx reload failed"


def get_nginx_config(container_dict):
    container_port = "80"
    config = ""
    for container_name in container_dict.keys():
        config = config + container_dict[container_name] + ":" + container_port + "," + "\n"

    logging.info("current config : " + config)
    return config


def stop_nginx():
    status = os.system(NGINX_SBIN_PATH + "/" + "nginx -s quit")

    if status == 0:
        logging.info("nginx stop success")
    else:
        logging.error("nginx stop failed")
