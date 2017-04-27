from util.DockerUtil import Container_status

if __name__ == '__main__':
    container = Container_status("aa", 1, 1, "192.168.1.1");
    container2 = Container_status()