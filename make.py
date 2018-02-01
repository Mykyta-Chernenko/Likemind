#!/usr/bin/env python

import os
import sys

import argparse


class DockerComposeWrap(object):

    def __init__(self, project_name):
        self.project_name = project_name
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('command')
        self.parser.add_argument('--compose-env')

    def execute(self):
        base_args, other_args = self.parser.parse_known_args()
        try:
            method = getattr(self, 'on_' + base_args.command)
        except AttributeError:
            self.on_help()
            return 1
        self._init_compose_files(base_args.compose_env)
        method(*other_args)

    def _init_compose_files(self, force_env):
        self.compose_files = ['docker-compose.yml']
        # if force_env:
        #     force_file = 'docker-compose.%s.yml' % force_env
        #     assert os.path.exists(force_file), 'No such file %s' % force_file
        #     self.compose_files.append(force_file)
        # else:
        #     if os.path.exists('docker-compose.local.yml'):
        #         self.compose_files.append('docker-compose.local.yml')
        #     else:
        #         self.compose_files.append('docker-compose.dev.yml')

    def on_help(self, *args):
        self.parser.print_usage()
        print('Available actions:')
        for i in dir(self):
            if i.startswith('on_'):
                print(' - ' + i[3:])

    def compose_cmd(self, cmd):
        docker_compose = 'docker-compose -f ' + ' -f '.join(self.compose_files)
        docker_compose += ' -p %s' % self.project_name
        self.shell(docker_compose + ' ' + cmd)

    def shell(self, cmd):
        print(' -> %s' % cmd)
        return os.system(cmd)


class DockerCtl(DockerComposeWrap):

    def on_runserver(self, *args):
        self.compose_cmd('up --build ' + ' '.join(args))

    def on_build(self, *args):
        self.compose_cmd('build')

    def on_down(self, *args):
        self.compose_cmd('down')

    def on_manage(self, *args):
        self.compose_cmd('exec backend python manage.py %s' % ' '.join(args))

    def on_exec(self, *args):
        self.compose_cmd('exec backend %s' % ' '.join(args))


ctl = DockerCtl('LikeMind')
ctl.execute()
