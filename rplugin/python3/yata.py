#!/usr/bin/env python
# coding: utf-8

import neovim
import os
import json
import shutil
import subprocess


@neovim.plugin
class YataVim(object):
    def __init__(self, vim):
        try:
            command, port = config(vim)
            self.__command = command
            self.__port = port
            self.__exception = None
        except CommandNotFound as exception:
            self.__exception = exception

    @neovim.function('_yata__run_if_needed', sync=True)
    def run_if_needed(self, args):
        if not self.__exception is None:
            return self.__exception.to_json()

        try:
            response = Client(self.__port).ping()
        except RequestFailed:
            command = [
                self.__command,
                'run',
                '--port', str(self.__port)
            ]
            try:
                execute(command)
            except:
                return CommandExecutionFailed(command).to_json()
            return {}

        server_name = response.get('name')
        if server_name != 'jp.mitsuse.Yata':
            return UnknownServerRunnning(self.__port, server_name).to_json()

        return {}


class Client(object):
    def __init__(self, port):
        self.__port = port
        self.__endpoint = 'http://localhost:{}/'.format(port)

    def complete(self, path, offset):
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
        except Exception as exception:
            raise RequestFailed(self.__port, request_body, exception)

        if response.status != 200:
            raise RequestFailed(
                self.__port,
                request_body,
                UnacceptableStatus(response.status)
            )

        return json.loads(response.read().decode())

    def ping(self):
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
        except Exception as exception:
            raise RequestFailed(self.__port, request_body, exception)

        if response.status != 200:
            raise RequestFailed(
                self.__port,
                request_body,
                UnacceptableStatus(response.status)
            )

        return json.loads(response.read().decode())


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
        raise CommandNotFound(path)

    return default


class CommandNotFound(Exception):
    def __init__(self, command):
        self.__command = command

    @property
    def command(self):
        return self.__command

    def to_json(self):
        return {
            'error': {
                'name': 'command_not_found',
                'message': 'command not found: {}'.format(self.command),
                'paramerters': {
                    'command': self.command
                }
            }
        }


class CommandExecutionFailed(Exception):
    def __init__(self, command):
        self.__command = command

    @property
    def command(self):
        return self.__command

    def to_json(self):
        return {
            'error': {
                'name': 'command_execution_failed',
                'message': 'command execution failed: {}'.format(
                    ' '.join(self.command)
                ),
                'paramerters': {
                    'command': self.command
                }
            }
        }


class RequestFailed(Exception):
    def __init__(self, port, request, exception):
        self.__port = port
        self.__request = request
        self.__exception = exception

    @property
    def port(self):
        return self.__port

    @property
    def request(self):
        return self.__request

    @property
    def exception(self):
        return self.__exception

    def to_json(self):
        return {
            'error': {
                'name': 'request_failed',
                'message': 'request failed: {}'.format(
                    self.port,
                    self.request,
                    self.exception
                ),
                'paramerters': {
                    'command': self.command
                }
            }
        }


class UnacceptableStatus(Exception):
    def __init__(self, status):
        self.__status = status


class UnknownServerRunnning(Exception):
    def __init__(self, port, name):
        self.__port = port
        self.__name = name

    @property
    def port(self):
        return self.__port

    @property
    def name(self):
        return self.__name

    def to_json(self):
        return {
            'error': {
                'name': 'unknown_server_running',
                'message': 'unknown server is running: port={}, name={}'.format(
                    self.port,
                    self.name
                ),
                'paramerters': {
                    'port': self.port,
                    'name': self.name
                }
            }
        }
