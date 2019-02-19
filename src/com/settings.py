#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from datetime import date
import datetime
from os.path import abspath, dirname

BPC_PATH = '/opt/bpc'
NPMDATA_PATH = '/opt/npm'
NPMWEB_PATH = '/opt/npmweb'
SMARTPROBE_PATH = '/opt/smartprobe/sp'

PROJECT_ROOT = abspath(dirname(__file__))

# green whale 172.16.14.22 可用
# blue whale 172.16.11.181
# red whale 172.16.14.24

TEST_VM_HOST = {
    'name': 'test_create_vm1_for_mycroft_own',
    'ip': '172.16.15.61/24',
    'project': 'npm3',
    'desc': 'npm3 unit test for mycroft',
    'gateway': '172.16.15.1',
    'dockerflyd_server': 'http://172.16.11.181:5123/v1/'
}

BASE_DOCKER_REPO = "docker-registry.dev.netis.com.cn:5000/autobuild/"
DATE_TAG = date.today().strftime("%Y%m%d")

if date.today().isoweekday() == 6:
    DATE_TAG = (date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
elif date.today().isoweekday() == 7:
    DATE_TAG = (date.today() - datetime.timedelta(days=2)).strftime("%Y%m%d")


IMAGE_NAME_MAP = {
    'centos6': BASE_DOCKER_REPO + 'centos6',
    #'bpc3': BASE_DOCKER_REPO + 'bpc3_source_anonymous_snapshot:' + DATE_TAG,
    'bpc3': BASE_DOCKER_REPO + 'bpc3_source_anonymous_snapshot:' + DATE_TAG,
    
    # ----------NPM branch---------------
    # blue whale
    'npm3': BASE_DOCKER_REPO + 'npm3_binary_anonymous_git_release:develop-' + DATE_TAG,
    # red whale
    #'npm3': BASE_DOCKER_REPO + 'npm3_source_ldap_git_snapshot:' + DATE_TAG,
 
    # ----------SP branch---------------
    # blue whale
    'smartprobe': BASE_DOCKER_REPO + 'smartprobe_binary_anonymous_git_release:develop-' + DATE_TAG,
    #'smartprobe': BASE_DOCKER_REPO + 'smartprobe_binary_anonymous_git_release:develop-v3.5.3-' + DATE_TAG,
    # red whale
    #'smartprobe': BASE_DOCKER_REPO + 'smartprobe_source_ldap_git_snapshot:' + DATE_TAG,
}

try:
    from local_settings import *
except ImportError:
    pass
