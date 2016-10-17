#!/usr/bin/env python
# coding: utf-8

import neovim
import os
import shutil
import subprocess


@neovim.plugin
class YataVim(object):
    def __init__(self, vim):
        command, port = config(vim)
        self.__command = command
        self.__port = port

    def is_running(self):
        response = Client(self.__port).ping()
        if response is None:
            return False
        return response.get('name') == 'jp.mitsuse.Yata'

    def run(self):
        execute([
            self.__command,
            'run',
            '--port', str(self.__port)
        ])

    @neovim.function('_yata__run_if_needed', sync=True)
    def run_if_needed(self, args):
        if self.is_running():
            return
        self.run()


class Client(object):
    def __init__(self, port):
        self.__endpoint = 'http://localhost:{}/'.format(port)

    def complete(self, path, offset):
        import json
        from urllib import request

        request_body = json.dumps(
            {
                'method': 'complete',
                'parameters': {
                    'file': {
                        'path': path
                    },
                    'offset': offset
                }
            }
        ).encode('utf-8')

        response = request.urlopen(
            request.Request(
                self.__endpoint,
                data=request_body,
                method='POST',
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }
            )
        )

        if response.status != 200:
            return []

        return json.loads(response.read().decode())

    def ping(self):
        import json
        from urllib import request

        request_body = json.dumps(
            {
                'method': 'ping',
                'parameters': {}
            }
        ).encode('utf-8')

        try:
            response = request.urlopen(
                request.Request(
                    self.__endpoint,
                    data=request_body,
                    method='POST',
                    headers={
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    }
                )
            )
            if response.status != 200:
                return None
            return json.loads(response.read().decode())
        except:
            return None


def config(vim):
    config = vim.vars['yata#config']
    command = validate_command(config.get('command', 'yata'))
    port = int(config.get('port', 9000))
    return (command, port)


def execute(command):
    subprocess.Popen(
        command,
        stdin=None,
        stdout=None,
        stderr=None,
        start_new_session=True
    )


def validate_command(path):
    if os.access(path, mode=os.X_OK):
        return path

    default = shutil.which(os.path.basename(path), mode=os.X_OK)
    if default is None:
        raise CommandNotFound(default)

    return default


class CommandNotFound(Exception):
    def __init__(self, command):
        self.__command = command

    @property
    def command(self):
        return self.__command
