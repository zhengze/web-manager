#import paramiko
from fabric.api import run, env, roles, execute, local
import os

#env.hosts = ['172.28.32.49:22', '172.28.32.50:22']
#env.user = "root"
#env.password = "123.com"


#IP="172.28.32.50"
#PORT=22
#USERNAME="root"
#PASSWORD="123.com"
#CMD="supervisorctl status"
#
#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect(IP, PORT, USERNAME, PASSWORD, timeout=5)
#stdin, stdout, stderr = ssh.exec_command(CMD)
#print stdout.readlines()
#ssh.close()

env.shell = True
env.executable = '/bin/bash'

env.roledefs = {
    'dev_crp' : ['172.28.32.32'],
    'test_lb' : ['172.28.32.51', '172.28.32.53'],
    'test_app' : ['172.28.32.51', '172.28.32.53'] 
}
 
env.user = 'root'
env.password = '123.com'

supervisorctl_status_cmd = "supervisorctl status"
keepalived_status_cmd = "systemctl status keepalived"
nginx_status_cmd = "systemctl status nginx"
uop_frontend_build_cmd = "npm run build"

@roles("dev_crp")
def dev_crp_status():
    run(supervisorctl_status_cmd)

@roles("test_lb")
def test_lb_status():
    #run(keepalived_status_cmd)
    try:
        run(nginx_status_cmd)
    except Exception as ex:
        print "error:", ex


def update_uop():
    root_path = "/home/zhengze/codes"
    uop_backend_path = "/".join([root_path, "uop-backend"])
    crp_backend_path = "/".join([root_path, "uop-crp"])
    uop_frontend_path = "/".join([root_path, "uop-frontend"])
    cmdb_frontend_path = "/".join([root_path, "cmdb-frontend"])
    cmdb_backend_path = "/".join([root_path, "cmdb-backend"])
    paths = [uop_backend_path, crp_backend_path, uop_frontend_path, cmdb_backend_path, cmdb_frontend_path]
        
    for path in paths:
        print
        local("cd "+path+";git branch;git pull")


def main():
    execute(update_uop)


if __name__ == "__main__":
    cmd = "fab -f update_code.py main"
    os.system(cmd)