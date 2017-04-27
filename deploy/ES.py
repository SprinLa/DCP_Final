import sys
import os
import logging

# import urllib2

# root

sudo_param = "sudo -u "
username = "es"

version = "2.4.1"
software_name = "elasticsearch"

path = "/usr/local/elasticsearch-" + version + "/"
pid_path = "/tmp/elasticsearch-pid"

config_name = "elasticsearch.yml"

data_configure = "path.data: /tmp/elasticsearch"
log_configure = "path.logs: /var/log/elasticsearch"  # need check

cluster_config = "discovery.zen.ping.unicast.hosts:"

LOG_FILE_PATH = '/data0/log/DCP_ESDeploy.log'

os.system("mkdir -p /data0/log")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')


def start():
    logging.info("elasticsearch start...")
    # value = os.system(path+"elasticsearch")
    value = os.system(sudo_param + username + " " + path + "bin/elasticsearch " + "-p " + pid_path + " -d")
    if value == 0:
        logging.info("elasticsearch start...OK")
    else:
        logging.error("start error!")


def status():
    value = os.popen("ps aux | grep elasticsearch | grep -v grep").read()
    if value == "":
        logging.error("elasticsearch is not started or something wrong")
    else:
        logging.info(status)


def stop():
    logging.info("elasticsearch stop...")
    value = os.popen("cat " + pid_path + " && echo").read()
    result = os.system("kill " + str(value))
    os.system("rm -rf " + pid_path)
    if result == 0:
        logging.info("elasticsearch stop...OK")
    else:
        logging.info("elasticsearch stop failed")


def init():
    logging.info("elasticsearch init...")

    # ip configure
    centos_version = os.popen("rpm -q centos-release | awk -F \"-\" '{print $3}'").read()
    ip = ""
    centos_version = centos_version[0:len(centos_version) - 1]
    if centos_version == "6":
        ip = os.popen(
            "ifconfig eth0 | grep \"inet addr\" | awk '{ print $2}' | awk -F: '{print $2}'").read()  # centos 7 may have some problems
    if centos_version == "7":
        ip = os.popen("ifconfig eth0 | grep \"inet\" | awk '{ print $2}'").read()

    network_host = os.popen("cat " + path + "config/" + config_name + " | grep network.host").read()
    network_host = network_host[0:len(network_host) - 1]
    ip_configure = "network.host: " + ip[0:len(ip) - 1]
    network_host_change = os.system(
        "sed -i s@\"" + network_host + "\"@\"" + ip_configure + "\"@g " + path + "config/" + config_name)
    if network_host_change == 0:
        logging.info("network.host changes successfully")
    else:
        logging.error("network.host changes unsuccessfully")
        return
    # node.name
    host_name = os.popen("hostname").read()
    host_name = host_name[0:len(host_name) - 1]
    if host_name == "":
        logging.error("Don't have a hostname...Failed")
        return
    else:
        node_name = os.popen("cat " + path + "config/" + config_name + " | grep node.name").read()
        node_name = node_name[0:len(node_name) - 1]
        node_name_configure = "node.name: " + host_name
        node_name_change = os.system(
            "sed -i s@\"" + node_name + "\"@\"" + node_name_configure + "\"@g " + path + "config/" + config_name)
        if node_name_change == 0:
            logging.info("node.name changes successfully")
        else:
            logging.error("node.name changes unsuccessfully")
            return


# discover.list
def cluster():
    cluster_list = os.popen("cat ../conf/dcp_es_cluster.conf").read()  #####!!!!!!!
    cluster_list = cluster_list[0:len(cluster_list) - 1]
    cluster_default = os.popen("cat " + path + "config/" + config_name + " | grep " + cluster_config).read()
    cluster_default = cluster_default[0:len(cluster_default) - 1]
    cluster_list_configure = cluster_config + cluster_list
    cluster_list_change = os.system(
        "sed -i s@\"" + cluster_default + "\"@\"" + cluster_list_configure + "\"@g " + path + "config/" + config_name)
    if cluster_list_change == 0:
        logging.info(cluster_list_configure + " changes successfully")
    else:
        logging.error(cluster_list_configure + " changes unsuccessfully")
        return


def printUsage():
    print "usage: options start"
    print "       options status"
    print "       options stop"
    print "       options init"
    print "       options cluster"
    print "       options launch"
    print "for example: python *.py start"


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if str(sys.argv[1]) == "start":
            start()
        elif str(sys.argv[1]) == "status":
            status()
        elif str(sys.argv[1]) == "stop":
            stop()
        elif str(sys.argv[1]) == "init":
            init()
        elif str(sys.argv[1]) == "cluster":
            cluster()
        elif str(sys.argv[1]) == "launch":
            init()
            cluster()
            start()
        else:
            printUsage()
    else:
        printUsage()
