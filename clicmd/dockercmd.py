#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import click
from src.com.docker import *
class DockerCMD(object):
    def connect(self, host):
        DockerClient().connect_host(host)
    
    def fabric_init(self, host):
        DockerClient().fabric_init(host)
    
    def fabric_run_cmd(self, cmd):
        DockerClient().fabric_run_command(cmd)

@click.command()
@click.option("--host",default='127.0.0.1')
def connect(host):
    DockerCMD().connect(host)
    click.echo('connected to host %s'% host)

@click.command()
@click.option('--host', default='127.0.0.1')
def fabric_init(host):
    DockerCMD().fabric_init(host)

@click.command()
@click.option('--host')
@click.option('--cmd')
def fabric_run_cmd(host, cmd):
    DockerCMD().fabric_init(host)
    DockerCMD().fabric_run_cmd(cmd)



