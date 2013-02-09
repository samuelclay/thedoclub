from __future__ import with_statement
from fabric.api import *
from contextlib import contextmanager as _contextmanager

env.hosts = ['thedoclub.com']
env.user = 'sclay'
env.keyfile = ['$HOME/.ssh/id_dsa']
env.directory = '/srv/thedoclub/'
env.activate = 'source /srv/thedoclub/bin/activate'

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

def deploy():
    with virtualenv():
        run('git pull')
        run('pip install -r requirements.txt')
        sudo('supervisorctl restart uwsgi')
        sudo('supervisorctl restart dccelery')
