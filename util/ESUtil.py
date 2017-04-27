from elasticsearch import Elasticsearch
import os
import logging

es = Elasticsearch([{'host': '172.17.0.11', 'port': 9200}])

LOG_FILE_PATH = '/data0/log/DCP.log'

os.system("mkdir -p /data0/log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')


def createMapping():
    request_mapping = ""

    try:
        mapping_file = open("../conf/ES_mapping.json")
        for line in mapping_file.readlines():
            request_mapping += line
    except Exception, e:
        logging.error(e)
        raise e

    else:
        mapping_file.close()

    logging.info("current index_mapping : \n" + request_mapping)

    status = es.indices.create(index="docker-test-mapping", ignore=400, body=request_mapping)

    logging.info(status)


def write2es(index="docker-test", doc_type="test", body=""):
    result = es.index(index, doc_type, body)
    logging.info(result)


if __name__ == '__main__':
    logging.info("ESUtil")
