import os
from os import path

from fabric.api import env, run, cd, local, lcd

CODE_DIR  = '/home/videalize/videalize-video-processor'
DEPLOY_DIR = '../deployment'
BRANCH = 'master'

def fetch_hosts():
    with lcd(DEPLOY_DIR):
        output = local('ansible tag_Name_video_processor --list-hosts -i inventory/production', capture=True)
        return [ip.strip() for ip in output.splitlines()[1:]]


env.user = 'videalize'
env.hosts = fetch_hosts()
env.key_filename = path.join(os.environ['HOME'], '.ssh', 'videalize')
env.use_ssh_config = True


def deploy():
    with cd(CODE_DIR):
        run("GIT_SSH_COMMAND='ssh -i ~/.ssh/video_processor_deploy' git fetch")
        sha = run("git rev-parse {0}".format(BRANCH))
        run("git checkout {0}".format(sha))

        pid = run("cat tmp/video_processor.pid")
        run("kill -SIGINT {0}".format(pid))
