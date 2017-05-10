import os


if __name__ == '__main__':
    os.system("rpm -Uvh http://dl.Fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm")
    os.system("yum -y install docker-io")
    os.system("service docker start")