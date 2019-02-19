#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from .machine import VMachine, VMStatus, LMachine
from .remote import RunInRemoteTask
from fabric.api import env, run
from fabric.operations import *
from fabric.context_managers import settings, hide
from fabric.state import connections
from robot.utils import asserts
from robot.api.deco import keyword
import time
import click

class DockerClient(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.blue_dockerfly = "http://172.16.11.181:5123/v1/"
        self.red_dockerfly = "http://172.16.14.24:5123/v1/"
        self.dockerfly = self.blue_dockerfly

    # class RunBackgroundCmdInRemoteTask(RunInRemoteTask):

    #     def executeBackground(self):
    #         return run(self._cmdline, pty=False)
    
    def createDocker(self, kwargs, safe=False):
        # 前台传入vm_info 创建docker
        vm_info = {
            'name': kwargs['id'],
            'ip': kwargs['ip'] + '/24',
            'project': kwargs['project'],
            'desc': kwargs['desc'],
            'gateway': kwargs['gateway'],
            'dockerflyd_server': kwargs['dockerflyd'],
            'group': kwargs.get('group', 'default')
#             'veths': kwargs.get('veths')
        }
        # 是否设置veths npm无需设置
        if kwargs.get('veths') != [None]:
            vm_info.update({'veths': kwargs.get('veths')})
        print vm_info  
        vm = VMachine(**vm_info)
        if safe:
            if vm.status == VMStatus.NOPRESENT:
                vm.create()
            else:
                print 'Docker already exist!'
        elif not safe:
            if vm.status != VMStatus.NOPRESENT:
                vm.delete()
            vm.create()
        return self

    def deleteDocker(self, **kwargs):
        vm_info = {
            'name': kwargs['id'],
            'ip': kwargs['ip'] + '/24',
            'project': kwargs['project'],
            'desc': kwargs['desc'],
            'gateway': kwargs['gateway'],
            'dockerflyd_server': kwargs['dockerflyd'],
            'group': kwargs.get('group', 'default'),
            'veths': kwargs.get('veths')
        }
        vm = VMachine(**vm_info)
        vm.delete()
        return self
    
    def deleteDockerByName(self, name):
        vm_info = {
            'name': name,
            'ip': '',
            'project': '',
            'desc': '',
            'gateway': '',
            'dockerflyd_server': self.dockerfly,
            'group': '',
            'veths': ''
        }
        vm = VMachine(**vm_info)
        vm.delete()
        return self
    
    def execute_command_on_vm(self, commands, machines, ip):
        vm_info = {
            'name': machines,
            'ip': ip+"/24",
            'project': '',
            'desc': '',
            'gateway': '',
            'dockerflyd_server': self.dockerfly,
            'group': '',
            'veths': ''
        }
        vm = VMachine(**vm_info)
        vm.execute(commands)
        return self
    
    
    # def put_file_to_vm(self, local_path, remote_path,machines, ip):
    #     vm_info = {
    #         'name': machines,
    #         'ip': ip+"/24",
    #         'project': '',
    #         'desc': '',
    #         'gateway': '',
    #         'dockerflyd_server': self.dockerfly,
    #         'group': '',
    #         'veths': ''
    #     }
    #     vm = VMachine(**vm_info)
    #     vm.putfile(local_path, remote_path)
    #     return self
    def put_file_to_host(self, local, remote):
        put(local, remote)
        return self

    def get_file_from_host(self, remote, local):
        get(remote, local)
        return self
    
    # def has_command(self, name):
    #     print has_command(name, kwargs=None)
    #     return self

    def fabric_init(self, host_string, user='root', password='rootroot'):
        env.host_string = host_string
        env.user = user
        env.password = password
        print env.host_string
        return self
    
    def fabric_run_command(self, cmd, _pty=None, _timeout=None):
        if _timeout is not None:
            timeout= _timeout
        else:
            timeout = 900
        if _pty is not None:
            with settings(warn_only=True):
                fabric_run_return = run(cmd, timeout, pty=_pty)
        else:
            with settings(warn_only=True):
                fabric_run_return = run(cmd, timeout)
        if fabric_run_return.return_code == 1:
            print "find run commnand received nonzero return code 1"
            asserts.fail(u"fabric 执行命令“%s”时候出错，" % (cmd))
        return self

    def fabric_run_command_and_return_value(self, cmd, _pty=None):
        if _pty is not None:
            with settings(warn_only=True):
                fabric_run_return = run(cmd, pty=_pty)
                return fabric_run_return
        else:
            with settings(warn_only=True):
                fabric_run_return = run(cmd)
                return fabric_run_return
        if fabric_run_return.return_code == 1:
            print "find run commnand received nonzero return code 1"
            asserts.fail(u"fabric 执行命令“%s”时候出错，" % (cmd))
        return self

    def connect_host(self, host):
        wait = 250
        timeout = 5
        attempts = int(round(float(wait) / float(timeout)))
        with settings(
            hide('running'),
            timeout=timeout,
            connection_attempts=attempts
        ):
            time.sleep(5)
            print("try connect to host %s" % host)
            connections.connect(host)
        return self

    def run_command_on_host(self, host, command, _pty=None):
        self.connect_host(host)
        self.fabric_run_command(command, _pty)
        return self

    def run_command_on_host_with_return_result(self, host, command, _pty=None):
        self.connect_host(host)
        result = self.fabric_run_command_and_return_value(command, _pty)
        return unicode(result, "utf-8")

    def install_bpc(self, dir, host):
        install_cmd = "cd /root/%s/;./autoinstall_bpc_master.sh" % dir
        self.run_command_on_host_with_return_result(host, install_cmd)
        return self

