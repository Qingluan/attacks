from fabric.api import *
from qlib.io import GeneratorApi
from qlib.log import L, LogControl
from termcolor import colored
import os
ROOT_PATH = "/opt/attacks/attack-halo-backup/vps_manager/"
env.roledefs = {str(i):['root@'+v] for i,v in enumerate(
    [i.strip() for i in open(os.path.join(ROOT_PATH,"server.list")).readlines() if i.strip() ])}

env.password = 'wj1dd**..530135'
#env.password = '0svM3CwhQ4B4'
#env.password = "pico2016server.."
@task
def list():
    for i in env.roledefs:
        L(i, env.roledefs[i][0], color='blue')



def test(so):
    try:
        res = run(so + " -v")
    except Exception as e:
        return False
    return True

def ex_cmd(cmd):
    L(colored("[-]",'green'),cmd, color='blue')
    res = run(cmd, quiet=True)
    L('[T]',env.host,colored('-'* (LogControl.SIZE[1] -24),'red'))
    L(res,color='green')

@task
@parallel
def shadowsocks():
    ex_cmd("yum install -y python ")
    ex_cmd()

@task
@parallel
def go():
    output.running = False
    local("ssh root@"+ env.host)


def generate_hosts_passwds_env(generators):
    global env

@task
@parallel
def build_msf():
    imsg = run("docker images | grep msf ", quiet=True)
    if not imsg:
        ex_cmd("docker pull phocean/msf", quiet=True)
    fs= run("docker ps -a | grep msf ", quiet=True).strip()
    if not fs:
        run("docker run --rm -i -t -p 9990-9999:9990-9999 -v /root/.msf4:/root/.msf4 -v /tmp/msf:/tmp/data --name msf phocean/msf")
    else:
        output.running= False
        local("ssh root@" + env.host  + "  `docker attach msf`")

@task
def list_user():
    ex_cmd("docker exec -it ipsec-vpn-server cat  /etc/ppp/chap-secrets /etc/ipsec.secrets ")


@task
@parallel
def up(f):
    put(f, "/tmp/")

@task
@parallel
def breakOs():
    ex_cmd("docker ps -a | awk '{print $1 }' | xargs docker rm -f ") 
    ex_cmd("docker images  | awk '{print $3 }' | xargs docker rmi -f ") 
    ex_cmd(" rm -rf /var/log ")
    ex_cmd(" rm  -rf ~/")
    ex_cmd(" rm -rf /tmp")
    ex_cmd(" rm -rf /opt")
    ex_cmd(" rm -rf /usr")
    ex_cmd(" rm -rf /home")
    ex_cmd(" rm -rf /bin")
    ex_cmd(" rm -rf /etc")
    ex_cmd(" rm -rf /srv")



@task
def adduser():
    user = input(colored("user:",'blue', attrs=['underline']))
    passwd = input(colored("passwd:",'blue', attrs=['underline']))
    passwd_nk = os.popen("openssl passwd -1 {passwd} ".format(passwd=passwd)).read().strip()
    L(colored("[*]",'yellow'), 'new psk:', passwd_nk, color='green', a=['bold'])

    #run("docker exec -it ipsec-vpn-server bash")
    ex_cmd("docker exec -it ipsec-vpn-server sed -i '$a \"{}\" l2tpd \"{}\" *'  /etc/ppp/chap-secrets".format(user, passwd))
    ex_cmd("docker exec -it ipsec-vpn-server sed -i '$a {user}:{xpasswd}:xauth-psk'  /etc/ipsec.d/passwd".format(user=user, xpasswd=passwd_nk))
    list_user()
    ex_cmd("docker restart ipsec-vpn-server ")
#    ex_cmd("docker exec -it  ipsec-vpn-server service ipsec restart ")

    list_user()



@task
@parallel
def vpn(build=False):
    output.running = False
    start_cmd = "docker run  --name ipsec-vpn-server --restart=always -p 500:500/udp  -p 4500:4500/udp  -v /lib/modules:/lib/modules:ro  -d --privileged  hwdsl2/ipsec-vpn-server"

    if build:
            ex_cmd("yum install -y  epel-release")
            ex_cmd("yum update -y")
            ex_cmd("yum install -y  docker-io")
            ex_cmd("service docker start")
            ex_cmd("docker pull hwdsl2/ipsec-vpn-server")
            ex_cmd("modprobe af_key")
    else:
            ex_cmd(start_cmd)
            ex_cmd("docker logs ipsec-vpn-server | head -n 17")

@task
def vpn_status():
    output.running = False
    ex_cmd("docker ps -a | grep vpn")
    ex_cmd("docker logs ipsec-vpn-server | head -n 18")
    ex_cmd("docker exec -it ipsec-vpn-server ipsec whack --trafficstatus")

@task
@parallel
def ex(cmd):
    output.running = False
    ex_cmd(cmd)





def main():
    args = GeneratorApi({
        'list': (False, 'list roles'),
        })
    


