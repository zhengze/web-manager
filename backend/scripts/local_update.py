#!/usr/bin/python env


from fabric.api import run, env, roles, execute, local, cd, parallel, task
import os

env.executable = '/bin/bash'


@task
@parallel
def update_uop():
    root_path = "/home/zhengze/codes"
    with cd(root_path):
        uop_backend_path = "/".join([root_path, "uop-backend"])
        crp_backend_path = "/".join([root_path, "uop-crp"])
        uop_frontend_path = "/".join([root_path, "uop-frontend"])
        paths = [uop_backend_path, crp_backend_path, uop_frontend_path]

        for path in paths:
            print
            local(
                "cd " +
                path +
                ";git fetch origin;git reset --hard HEAD;git pull")


def main():
    execute(update_uop)


if __name__ == "__main__":
    cmd = "fab -f update_code.py main"
    os.system(cmd)