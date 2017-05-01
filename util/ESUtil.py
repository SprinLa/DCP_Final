from elasticsearch import Elasticsearch
import os
import logging
from ConfigUtil import Properties


dcp_init_config = Properties("../conf/dcp_init.conf").getProperties()
network_list = dcp_init_config["es.network.cluster"]

es = Elasticsearch([{'host': network_list, 'port': 9200}])

LOG_FILE_PATH = '/data0/log/DCP.log'

os.system("mkdir -p /data0/log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')


def write2es(index="docker-test", doc_type="test", body=""):
    result = es.index(index, doc_type, body)
    logging.info(result)


if __name__ == '__main__':
    dcp_init_config = Properties("../conf/dcp_init.conf").getProperties()
    network_list = dcp_init_config["es.network.cluster"]
