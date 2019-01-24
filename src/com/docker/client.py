#!/usr/bin/env python
#  -*- coding: utf-8 -*-


from src.com.apis import create_docker, run, has_command
# from mycroft.framework.utils import import_object
# from mycroft.packages.old.core.client.machine import VMachine, VMStatus, LMachine
from .machine import VMachine, VMStatus, LMachine
# from mycroft.packages.old.core.client.remote import RunInRemoteTask
from .remote import RunInRemoteTask


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

    class RunBackgroundCmdInRemoteTask(RunInRemoteTask):

        def executeBackground(self):
            return run(self._cmdline, pty=False)
    
    def createDocker(self, kwargs, safe=False, create=True):
#     def createDocker(self, **kwargs):
        #         def create_docker(self):
        #         self.vm = self._get_new_vm()
        #         self.vm.create()
        #         self.vm.execute('/usr/local/bin/npmtt setup')
        
#         print kwargs
#         create_docker(kwargs, safe=False, create=True)
#         return self
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
        
        print "+++++++++++++++++++++++++++++++++++"
        if kwargs.get('veths') != [None]:
            vm_info.update({'veths': kwargs.get('veths')})
        print vm_info
        print "+++++++++++++++++++++++++++++++++++"
        
        vm = VMachine(**vm_info)
        if create:
            if safe:
                if vm.status == VMStatus.NOPRESENT:
                    vm.create()
            elif not safe:
                if vm.status != VMStatus.NOPRESENT:
                    vm.delete()
                vm.create()
#       return vm
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
    
    def execute_command_on_vm(self, execute_type, commands, machines, ip):
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
#         vms = []
#         vms.append(vm)
#         run("Execute", {execute_type:commands}, vms)
        vm.execute(commands)
#         vm.execute('/usr/local/bin/npmtt setup')
#         vm.execute('npm restart')
#         run(name, kwargs, vms)
        return self
    
    
    def put_file_to_vm(self, local_path, remote_path,machines, ip):
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
        vm.putfile(local_path, remote_path)
        return self
    
    def get_file_from_vm(self):
        pass
    
    def has_command(self, name):
        print has_command(name, kwargs=None)
        return self
