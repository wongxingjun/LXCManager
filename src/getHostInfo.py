'''
Created on Mar 21, 2014

@author: wangxingjun
'''

#!/usr/bin/env python  
# coding=utf-8 

import os
import libvirt
import platform
import socket

def getHostname():
    """
    Get host name
    """
    return socket.gethostname()


def getOS():
    """
    Get host machine OS information
    """
    os_ver=' '.join(platform.linux_distribution())
    os_bit=platform.architecture()[0]
    os_arc=platform.machine()
    return ' '.join([os_ver,os_bit,os_arc])



def getCpu():
    """
    Get host machine CPU information
    """
    f = open('/proc/cpuinfo')     
    lines = f.readlines()     
    f.close()  
    for line in lines:
        if line.rstrip('\n').startswith('model name'):
            cpu = line.rstrip('\n').split(':')[1]
    return cpu



def getProcessor(): 
    """
    Get processors information of the host machine
    """ 
    f = open('/proc/cpuinfo')     
    lines = f.readlines()     
    f.close()     
    count = 0     
    for line in lines:    
        line = line.lower().lstrip()     
        if line.startswith('processor'):     
            count = count + 1     
    return count



def getHardDisk():
    """
    Get hard disk information of the host machine
    """
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            harddisk_=(line.split()[1:5])
            break
    DISK_total =str(harddisk_[0])
    DISK_used = str(harddisk_[1])
    # DISK_perc = DISK_stats[3]
    return ''.join([DISK_total,'(',DISK_used,' Used)'])



def getMemory():
    """
    Get memory information of the host machine
    """
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            memory_=(line.split()[1:4])
            break
    mem_total = str(round(int(memory_[0]) / 1000, 1))
    mem_used = str(round(int(memory_[1]) / 1000, 1))
    # RAM_free = round(int(memory[2]) / 1000, 1)
    return ''.join([mem_total,'M(',mem_used,'M Used)'])


# libvirt verion  
def getLibvirtVer():
    return libvirt.getVersion()



def getInfo():
    """
    A summary of host information
    """
    hostname = getHostname()    
    OS= getOS()    
    CPU = getCpu().strip()   
    processor = getProcessor()    
    harddisk= getHardDisk()        
    memory= getMemory()           
    libvirt = getLibvirtVer()       
    res=[hostname,OS,CPU,processor,harddisk,memory,libvirt]
    return  res    
