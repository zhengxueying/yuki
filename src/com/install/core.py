#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import ConfigParser
import re
import os

BPC4_BASE = 'http://10.1.2.12:8080/package_chest/release/'

class InstallPackage(object):

    def __init__(self):
        pass

    def get_pkg_url(self, version, product='bpc'):
        filedir = os.path.split(os.path.realpath(__file__))[0]
        configPath = os.path.join(filedir, 'versions_map.ini')
        config = ConfigParser.ConfigParser()
        config.read(configPath)
        if product.lower() == 'bpc':
            ver = config.get('bpcmap', version)
            url =  BPC4_BASE + ver + '.tar.gz'
            print url
            return ver, url
        else:
            pass

    def get_os(self):
        try:
            with open('/etc/redhat-release', 'r') as redhat:
                redhat_release = redhat.read().strip()
    
            version = re.search('[release|Linux] (\d+.\d+)', redhat_release).groups()[0]
    
            if version.startswith('5'):
                return 'el5'
            elif version.startswith('6'):
                return 'el6'
            elif version.startswith('7'):
                return 'el7'
            else:
                return 'unknown'
        except Exception:
            raise SystemError('unknown system')
    
