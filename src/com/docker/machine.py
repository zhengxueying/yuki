#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import os
import shutil
import subprocess
from random import random

from .ippool import get_free_ips
from .container import Container, ContainerList
from .errors import (NoFreeIpException,
                     NoSupportProjectException,
                     ContainerStatusException)
from .remote import (RemoteEnv,
                     PutFileToRemoteTask,
                     GetFileFromRemoteTask,
                     RunInRemoteTask,
                     CheckFileExistsRemoteTask,
                     DelFileFromRemoteTask)

from .supervisor.rpc import SupervisorRpcClient

def check_if_running(func):
    def _check(*arg, **kws):
        if arg[0].status != VMStatus.RUNNING:
            raise ContainerStatusException('Container is not running')
        else:
            return func(*arg, **kws)
    return _check

class VMStatus(object):
    NOPRESENT = 1
    STOPPED = 2
    RUNNING = 3


class LMachine(object):

    def create(self):
        pass

    def recreate(self):
        pass

    def delete(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    @check_if_running
    def execute(self, command):
        subprocess.call(command, shell=True)

    @check_if_running
    def putfile(self, local_path, remote_path):
        shutil.copy(local_path, remote_path)

    @check_if_running
    def getfile(self, remote_path, local_path):
        shutil.copy(remote_path, local_path)

    @check_if_running
    def deletefile(self, remote_path):
        shutil.rmtree(remote_path)

    @check_if_running
    def checkfile_exists(self, remote_path):
        return os.path.exists(remote_path)

    @property
    def ip(self):
        return "127.0.0.1"

    @property
    def status(self):
        return VMStatus.RUNNING

    @property
    def user(self):
        return None

    @property
    def password(self):
        return None

    @property
    def id(self):
        return None

    @property
    def name(self):
        return None

    @property
    def project(self):
        return None

    @property
    def supervisor(self):
        return None

    @property
    def group(self):
        return None


class VMachine(object):

    supported_projects = ['centos6', 'bpc3', 'npm3', 'smartprobe']

    def __init__(self, name, gateway,
                       project,
                       desc='',
                       ip=None,
                       user='root',
                       password='rootroot',
                       dockerflyd_server='http://127.0.0.1:5123/v1/',
                       group=None,
                       veths=None):

        if ip is None:
            free_ips = get_free_ips(dockerflyd_server)
            if not free_ips:
                raise NoFreeIpException()
            else:
                self._ip = free_ips[int(random() * len(free_ips))]
        else:
            self._ip = ip

        self._name = name
        self._gateway = gateway
        self._veths = veths
        self._project = project
        self._desc = desc
        self._user = user
        self._password = password
        self._dockerflyd_server = dockerflyd_server
        self._group = group

        self._container = Container(self._name,
                                    self._ip,
                                    self._gateway,
                                    self._veths,
                                    self._project,
                                    self._desc,
                                    self._dockerflyd_server)

        if self.status == VMStatus.RUNNING:
            self._env = RemoteEnv(self._ip.split('/')[0], self._user, self._password)

        self._supervisor = SupervisorRpcClient(self._ip.split('/')[0])

    def create(self):
        if self.status == VMStatus.NOPRESENT:
            self._container.create()
            self._env = RemoteEnv(self._ip.split('/')[0], self._user, self._password)
        else:
            raise ContainerStatusException('Container is existing')

    def recreate(self):
        """
        if the same name of vm has existed, delete and recreate
        """
        if self.status != VMStatus.NOPRESENT:
            self.delete()
        self.create()

    def delete(self):
        if self.status != VMStatus.NOPRESENT:
            self._container.delete()
            self._status = VMStatus.NOPRESENT
        else:
            raise ContainerStatusException('Container has not existed')

    def start(self):
        if self.status == VMStatus.STOPPED:
            self._container.start()

    def stop(self):
        if self.status == VMStatus.RUNNING:
            self._container.stop()

    @check_if_running
    def execute(self, command):
        with RunInRemoteTask(self._env,
                             command) as task:
            return task.execute()

    @check_if_running
    def putfile(self, local_path, remote_path):
        with PutFileToRemoteTask(self._env,
                                 local_path,
                                 remote_path) as task:
            task.execute()

    @check_if_running
    def getfile(self, remote_path, local_path):
        with GetFileFromRemoteTask(self._env,
                                   remote_path,
                                   local_path) as task:
            task.execute()

    @check_if_running
    def deletefile(self, remote_path):
        with DelFileFromRemoteTask(self._env,
                                   remote_path) as task:
            task.execute()

    @check_if_running
    def checkfile_exists(self, remote_path):
        with CheckFileExistsRemoteTask(self._env,
                                       remote_path) as task:
            return task.execute()


    @property
    def ip(self):
        return self._ip.split('/')[0]

    @property
    def status(self):
        status = self._container.status
        if status == 'stopped':
            return VMStatus.STOPPED
        elif status == 'running':
            return VMStatus.RUNNING
        else:
            return VMStatus.NOPRESENT

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def id(self):
        return self._container.id

    @property
    def name(self):
        return self._name

    @property
    def project(self):
        return self._project

    @property
    def supervisor(self):
        return self._supervisor

    @property
    def group(self):
        return self._group
