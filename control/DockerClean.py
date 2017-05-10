import os

if __name__ == '__main__':
    os.system("docker rm -f $(docker ps -q)")
    os.system("docker network rm es_network app_network")