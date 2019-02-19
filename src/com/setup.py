#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from setuptools import setup, find_packages
setup(
    name = 'docker',
    version = '0.1',
    packages = find_packages('docker'),
    package_dir = {'':'docker'},
    include_package_data = True,
    install_requires = [
        'Click',
    ],
    entry_points = '''
        [console_scripts]
        conn=docker.client.DockerClient:connect_host
        hello=docker.client:hello
        test=docker.client:test_hello
    ''',
)