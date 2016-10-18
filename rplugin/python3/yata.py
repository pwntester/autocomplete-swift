#!/usr/bin/env python
# coding: utf-8

import neovim
import os
import json
import shutil
import subprocess


@neovim.plugin
class Service(object):
    def __init__(self, vim):
        try:
            self.__config = Service.load_config()
            self.__exception = None
        except Exception as exception:
            self.__exception = exception

    @neovim.function('_yata__run_if_needed', sync=True)
    def run_if_needed(self, args):
        if not self.__exception is None:
            return self.__exception.to_json()

        variables = os.environ.copy()
        variables['TOOLCHAINS'] = self.__config.toolchains

        try:
            response = Client(self.__config.port).ping()
        except RequestFailed:
            command = [
                self.__config.command,
                'run',
                '--port', str(self.__config.port)
            ]
            try:
                execute(command, variables)
            except:
                return CommandExecutionFailed(command).to_json()
            return {}

        server_name = response.get('name')
        if server_name != 'jp.mitsuse.Yata':
            return UnknownServerRunnning(self.__config.port, server_name).to_json()

        return {}

    @neovim.function('_yata__restart', sync=True)
    def restart(self, args):
        if not self.__exception is None:
            return self.__exception.to_json()

        try:
            response = Client(self.__config.port).ping()
        except RequestFailed:
            return self.run_if_needed([])

        server_name = response.get('name')
        server_pid = response.get('pid')
        if server_name != 'jp.mitsuse.Yata' or server_pid is None:
            return UnknownServerRunnning(self.__config.port, server_name).to_json()

        command = ['kill', '--TERM', str(server_pid)]
        try:
            execute(command, variables=None).communicate()
        except:
            return CommandExecutionFailed(command).to_json()
        return self.run_if_needed([])

    @staticmethod
    def load_config():
        try:
            path_config = os.path.expandvars('$HOME/.yata/config.json')
            with open(path_config) as f:
                json_config = json.load(f)
        except Exception as exception:
            raise ConfigLoadingFailed(path_config, exception)
        return Config(json_config)


class Config(object):
    def __init__(self, dictionary):
        try:
            self.__port = dictionary.get('port', 9000)
            self.__command = os.path.expandvars(dictionary.get('command', 'yata'))
            self.__toolchains = dictionary.get(
                "toolchains",
                "com.apple.dt.toolchain.Swift_2_3"
            )
            self.__environments = list(
                map(lambda o: Environment(o), dictionary.get('environments', []))
            )
        except Exception as exception:
            raise InvalidConfig()
        if not (
            type(self.__port) is int and
            type(self.__command) is str and
            type(self.__toolchains) is str and
            type(self.__environments) is list
        ):
            raise InvalidConfig()

    @property
    def port(self):
        return self.__port

    @property
    def toolchains(self):
        return self.__toolchains

    @property
    def command(self):
        return self.__command

    @property
    def environments(self):
        return self.__environments


class Environment(object):
    def __init__(self, dictionary):
        try:
            self.__name = dictionary['name']
            self.__toolchains = dictionary['toolchains']
        except Exception as exception:
            raise InvalidConfig()
        if not (type(self.__name) is str and type(self.__toolchains) is str):
            raise InvalidConfig()

    @property
    def name(self):
        return self.__name

    @property
    def toolchains(self):
        return self.__toolchains


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


def execute(command, variables):
    return subprocess.Popen(
        command,
        stdin=None,
        stdout=None,
        stderr=None,
        start_new_session=True,
        env=variables
    )


class InvalidConfig(Exception):
    def __init__(self):
        pass

    def to_json(self):
        return {
            'error': {
                'name': 'invalid_config',
                'message': 'invalid configuration'
            }
        }


class ConfigLoadingFailed(Exception):
    def __init__(self, path, exception):
        self.__path = path
        self.__exception = exception

    @property
    def path(self):
        return self.__path

    @property
    def exception(self):
        return self.__exception

    def to_json(self):
        return {
            'error': {
                'name': 'config_loading_failed',
                'message': 'failed loading configuration: path={}, exception={}'.format(
                    self.path,
                    self.exception
                ),
                'paramerters': {
                    'path': self.path,
                    'exception': str(self.exception),
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
                'message': 'request failed: port={}, request={}, exception={}'.format(
                    self.port,
                    self.request,
                    self.exception
                ),
                'paramerters': {
                    'port': self.port,
                    'request': str(self.request),
                    'exception': str(self.exception)
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
