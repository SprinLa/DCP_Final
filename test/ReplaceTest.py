import os

PATH = "/Users/wen/Downloads/test.conf"
SUBNET = "172.17.0"

if __name__ == '__main__':
    node_name = os.popen("cat " + PATH + " | grep  \"server " + SUBNET + "\"").read()
    node_name = node_name[0:len(node_name) - 1]
    print node_name
    node_name_configure = "server 172.17.0.3:80;\nserver 172.13.0.3:80;\n"
    conf_file = open(PATH, 'r')
    all_lines = conf_file.read()
    print all_lines
    new_lines = all_lines.replace(node_name, node_name_configure)
    # all_lines.replace("upstream localhost{", "1")
    print new_lines
    # conf_file.write(all_lines)
    conf_file.close()
    conf_file_w = open(PATH, "w")
    conf_file_w.write(new_lines+"\n")

    # print "sed -i s@\"" + str(node_name) + "\"@\"" + node_name_configure + "\"@g " + PATH
    # node_name_change = os.system("sed -i s@\"" + str(node_name) + "\"@\"" + node_name_configure + "\"@g " + PATH)
