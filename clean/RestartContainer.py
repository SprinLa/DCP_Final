from util.DBUtil import selectAll
from util.DockerUtil import restart_container

DCP_DB_PATH = "dcp_container"

if __name__ == "__main__":
    container_list = selectAll(DCP_DB_PATH)
    for container in container_list:
        restart_container(container)
