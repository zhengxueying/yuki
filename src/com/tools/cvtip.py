#!/usr/bin/python
# -*- coding: UTF-8 -*-
import struct
import socket
import click
import re

@click.command()
@click.option('--ip')
def convert_ip(ip):
    # convert ip to int
    if checkip(ip):
        intip = struct.unpack('!i', socket.inet_aton(ip))[0]
        print intip
    #convert int to ip 
    else:
        ipaddr = socket.inet_ntoa(struct.pack('I',socket.htonl(int(ip))))
        print ipaddr
    # else:
    #     print 'Wrong IP!'

def checkip(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False

if __name__ == "__main__":
    print convert_ip('10.32.176.21')