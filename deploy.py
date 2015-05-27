#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from fabric.api import env, run, sudo, task
from fabric.context_managers import cd, settings
from fabric.contrib import files

env.hosts = ['pypi01', 'pypi02']


@task(default=True)
def status():
    run('supervisorctl status | grep pypiserver')


@task
def rebuild():
    with cd('/data/apps/pypiserver'):
        with settings(sudo_user='zhihu'):
            sudo('python bootstrap.py')
            sudo('bin/buildout')


@task
def update_code():
    with cd('/data/apps/pypiserver'):
        with settings(sudo_user='zhihu'):
            sudo('git checkout master')
            sudo('git pull --ff-only origin master')
            sudo('bin/buildout')
            sudo('ln -sf /data/apps/pypiserver/etc/pypi.supervisor /data/etc/supervisor/conf.d/pypiserver.conf')


@task
def update_supervisor():
    with settings(warn_only=True):
        run('supervisorctl update')


@task
def restart():
    run('supervisorctl restart pypiserver')
    time.sleep(10)
    status()


def clone_code():
    with cd('/data/apps'):
        with settings(sudo_user='zhihu'):
            sudo('git clone --depth 1 https://github.com/lfyzjck/pypiserver.git')
            sudo('ln -sf /data/apps/pypiserver/etc/pypi.supervisor /data/etc/supervisor/conf.d/pypiserver.conf')


@task
def install_requirements():
    pass


@task
def deploy():
    if not files.exists('/data/apps/pypiserver'):
        clone_code()
        install_requirements()
        rebuild()
    update_code()
    update_supervisor()
    restart()
