import os
from os import path
import json

from fabric.api import env, run, cd, local, lcd

CODE_DIR  = '/home/videalize/videalize-video-processor'
DEPLOY_DIR = '../deployment'
BRANCH = 'master'
PYTHON = '{0}/venv/bin/python'.format(CODE_DIR)
PIP = '{0}/venv/bin/pip'.format(CODE_DIR)

def _fetch_hosts():
    with lcd(DEPLOY_DIR):
        output = local('python inventory/production', capture=True)
        return json.loads(output)

HOSTS = _fetch_hosts()
env.user = 'videalize'
env.hosts = HOSTS['tag_Name_video_processor']
env.key_filename = path.join(os.environ['HOME'], '.ssh', 'videalize')
env.use_ssh_config = True

def _is_production():
    return env.host_string in HOSTS['tag_Env_production']

def deploy():
    with cd(CODE_DIR):
        run("GIT_SSH_COMMAND='ssh -i ~/.ssh/video_processor_deploy' git fetch")
        if _is_production():
            sha = run("git rev-parse origin/{0}".format(BRANCH))
            run("git checkout {0}".format(sha))

            run("{0} install -r requirements.txt".format(PIP))
            run("{0} setup.py install".format(PYTHON))

            pid = run("cat tmp/video_processor.pid")
            run("kill -SIGINT {0}".format(pid))
        else:
            run("git checkout {0}".format(BRANCH))
            run("git merge origin/{0}".format(BRANCH))
            run("{0} install -r requirements.txt".format(PIP))
