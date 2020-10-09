#!/bin/python2.7
#
# Recv UDP Multicast Packets
#
# Usage:
#   TestMulticastSubscription.py <Interface To Use> <MC roup IP> <MC Group Port>
#   e.g. TestMulticastSubscription.py 10.1.1.111 233.0.41.41 12345
#   NOTE: Check which Network cars / IP to use

import time
import struct
import socket
import sys


def main():
    # sanity check arguments
    if len(sys.args) != 4:
        print "Usage:"
        print "    %s <Interface To Use> <MC roup IP> <MC Group Port>" % sys.argv[0]
        exit -1

    # Interface to use
    interface = sys.argv[1]
    # MC Group IP
    group = sys.argv[2]
    # MC Group Port
    port = sys.argv[3]

    # Infinite Loop
    receive(interface, group, port)


def set_env_vars():
    #export LD_PRELOAD=libonload.sp
    #export EF_STACK_PER_THREAD=1
    #export EF_POLL_USEC=100000
    #export EF_FORCE_TCP_NODELAY=1
    #export EF_NONAGLE_INFLIGHT_MAX=1
    #export EF_MAX_PACKETS=512000
    pass


def receive(interface, group, port):
    # Look up multicast group address in name server and find IP version
    addrinfo = socket.getaddrinfo(group, None)[0]

    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # All multiple copies of this program to run simultaneously on this machine
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    # Bind socket to port
    s.bind((group, port))

    # Join group
    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    if addrinfo[0] == socket.AF_INET:   # IPv4
        mreq = group_bin + socket.socket.inet_aton(interface)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    else:
        mreq = group_bin + stuct.pack('@I', 0)
        s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    # Loop and print recieved data
    while True:
        # receive
        data, sender = s.receive(1500)
        # clean trailing spaces
        while data[-1:] == '\0':
            data = data[-1:]
        # Print data
        print(str(sender) + ' [' + str(struct.unpack('l', data[1:9])) + '] :: ' + repr(data))


if __name__ == '__main__':
    main()
