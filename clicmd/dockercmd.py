#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import click
from src.com.docker.client  import DockerClient
from fabric.api import env, run 
from functools import update_wrapper
from src.com.install.core import InstallPackage
import os

cur_path = os.path.dirname(__file__)
SHELLPATH = '\\'.join([cur_path,'..\\src\\shell'])

@click.group(chain=True)
def cli():
    pass

@cli.resultcallback()
def process_cmd(processors):
    stream = ()
    for processor in processors:
        if processor:
            stream = processor(stream)
        else:
            pass

@cli.command('host')
@click.option('-h','--host' ,help='host to connect')
@click.option('-u','--user', default='root', help='username to connnect the host')
@click.option('-p','--passwd', default='rootroot', help='password of user')
def conn_host(host, user, passwd):
    env.host_string = host
    env.user = user
    env.password = passwd

@cli.command('cmd')
@click.option('-c', '--cmd',help='commond to run')
# @fabric_init
def fabric_run_cmd(cmd):
    # env.host_string = host
    DockerClient().fabric_run_command(cmd)
    return

@cli.command('install')
@click.option('-p','--product', default='bpc')
@click.option('-v','--version')
def install(product, version):
    ver, url =  InstallPackage().get_pkg_url(version, product)
    install_dir = os.path.join('/home','%s_%s'%(product, version)).replace('\\', '/')
    DockerClient().fabric_run_command('mkdir -p %s'% install_dir)
    DockerClient().fabric_run_command('cd %s;wget %s'% (install_dir,url))
    DockerClient().fabric_run_command('cd %s; tar zxvf %s.tar.gz'% (install_dir, ver))
    DockerClient().fabric_run_command('yum -y install expect')
    # cur_path = os.path.dirname(__file__)
    # file_dir = '\\'.join([cur_path,'..\\src\\shell\\autoinstall_bpc_master_4.3.x.sh'])
    file_dir = '\\'.join([SHELLPATH, 'autoinstall_bpc_master_4.3.x.sh'])
    DockerClient().put_file_to_host(file_dir,'%s/%s'%(install_dir,ver))
    DockerClient().fabric_run_command('chmod +x %s/%s/autoinstall_bpc_master_4.3.x.sh'%(install_dir,ver))
    DockerClient().fabric_run_command('cd %s/%s;./autoinstall_bpc_master_4.3.x.sh'%(install_dir,ver))

@cli.command('lic')
@click.option('-l', '--lic', is_flag=True)
def update_lic(lic):
    if lic:
        lic_file_path = '\\'.join([SHELLPATH, 'getlic_bpc_digest.sh'])
        DockerClient().put_file_to_host(lic_file_path, '/home')
        DockerClient().fabric_run_command('chmod +x /home/getlic_bpc_digest.sh;/home/getlic_bpc_digest.sh')

@cli.command('shm')
@click.option('-m', '--shm', default=4)
def change_shm(shm):
    DockerClient().fabric_run_command("sed -i 's#<shareHwm unit=\"MB\">[0-9]*</shareHwm>#<shareHwm unit=\"MB\">%d</shareHwm>#g' /opt/bpc/etc/system/local/pktminer.xml"%shm)

@cli.command('proto')
@click.option('--proto')
def update_protocol(proto):
    pass