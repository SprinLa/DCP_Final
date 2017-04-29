import logging
import os
from util.DBUtil import selectAll, bulk_delete
from util.DockerUtil import remove_container
from util.NginxUtil import get_nginx_config, nginx_reload, stop_nginx

DCP_DB_PATH = "dcp_container"
DCP_CONF_PATH = "dcp_conf"
ES_DB_PATH = "dcp_es"

LOG_FILE_PATH = '/data0/log/DCP_uninstall.log'

os.system("mkdir -p /data0/log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='w')


def uninstall():
    app_container_list = selectAll(DCP_DB_PATH)
    es_container_list = selectAll(ES_DB_PATH)

    for container_name in app_container_list.keys():
        remove_container(container_name)
        logging.info("remove " + container_name)

    # stop falcon and collect
    logging.info("start to stop falcon and collect")
    command = "ps aux | grep Deploy | awk '{ print $2 }'"
    pid = os.popen(command).read()
    if pid:
        logging.info("kill pid : " + pid)
        os.system("kill -9 " + pid)
    else:
        logging.warn("can't find falcon and collect pid")

    # remove es container
    logging.info("start to clear es cotainers")
    for container_name in es_container_list.keys():
        remove_container(container_name)
        logging.info("remove " + container_name)

    # delete from db
    bulk_delete(DCP_DB_PATH, app_container_list)
    bulk_delete(ES_DB_PATH, es_container_list)

    # nginx stop
    logging.info("start to stop nginx")
    config = get_nginx_config({})
    nginx_reload(config)
    stop_nginx()


if __name__ == '__main__':
    uninstall()
