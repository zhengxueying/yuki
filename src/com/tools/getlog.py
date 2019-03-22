#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import argparse
import time
import os
import subprocess

now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
suffix = time.strftime("%Y%m%d%H%M%S", time.localtime())

def getlog(app, start, end, tar):
    app = app.lower()
    os.system('mkdir -p /home/log_%s_%s' % (app, suffix))
    subprocess.call("cd /opt/%s/var/log;find . -name '*_stderr.log*'|xargs -I@ sh -c 'sed -n \"/%s/,/%s/p\" @ > /home/log_%s_%s/@'"%(app,start,end,app,suffix), shell=True)
    os.system('find /home/log_%s_%s -name "*.log*" -type f -size 0c|xargs -n 1 rm -f'% (app, suffix))
    if tar:
        os.system('tar zcPf /home/log_%s_%s.tar.gz /home/log_%s_%s/*'%(app, suffix, app, suffix))
        os.system('rm -rf /home/log_%s_%s'%(app, suffix))
    else:
        pass

def main():
    parser = argparse.ArgumentParser(description='getlog v1.0 按时间范围收集日志')

    parser.add_argument('app', help=u'收集日志的应用，支持:smartprobe/npm/npmweb')
    parser.add_argument('--start', dest='start', required=True, help=u'收集日志的开始时间,格式YYYY-MM-DD HH:mm:ss')
    parser.add_argument('--end', dest='end', default=now, help=u'收集日志的结束时间,格式YYYY-MM-DD HH:mm:ss')
    parser.add_argument('--tar', dest='tar', action='store_true', help=u'是否压缩收集的日志文件')

    args = parser.parse_args()
    getlog(args.app, args.start, args.end, args.tar)

if __name__ == "__main__":
    main()
