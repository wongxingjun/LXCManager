'''
Created on Mar 21, 2014

@author: wangxingjun
'''

#!/usr/bin/env python  
# coding=utf-8

from xml.dom.minidom import Document
import viewCon
import os
import getpass
import MySQLdb
import time

def genXML(s):
    """
    Generate a setting file for the container to be defined from s
    """
    doc = Document()
    #root
    domain = doc.createElement("domain")
    domain.setAttribute("type", "lxc")
    doc.appendChild(domain)
    #name
    name=doc.createElement("name")
    node=doc.createTextNode(s["name"]) 
    name.appendChild(node)
    domain.appendChild(name)
    #memory
    memory=doc.createElement("memory")
    node=doc.createTextNode(s["maxMem"]) 
    memory.appendChild(node)
    domain.appendChild(memory)
    
    #currentMemory
    curMem=doc.createElement("currentMemory")
    node=doc.createTextNode(s["curMem"])
    curMem.appendChild(node)
    domain.appendChild(curMem)
    
    #memtune
    memtune=doc.createElement("memtune")
    
    hard_limit=doc.createElement("hard_limit")
    node=doc.createTextNode(s["hard_limit"])
    hard_limit.appendChild(node)
    memtune.appendChild(hard_limit)
    
    soft_limit=doc.createElement("soft_limit")
    node=doc.createTextNode(s["soft_limit"])
    soft_limit.appendChild(node)
    memtune.appendChild(soft_limit)
    
    swap_hard_limit=doc.createElement("swap_hard_limit")
    node=doc.createTextNode(s["swap_hard_limit"])
    swap_hard_limit.appendChild(node)
    memtune.appendChild(swap_hard_limit)
    
    domain.appendChild(memtune)
    
    
    #vcpus
    vcpu=doc.createElement("vcpu")
    node=doc.createTextNode(s["vcpus"]) 
    vcpu.appendChild(node)
    domain.appendChild(vcpu)
    
    #cputune
    cputune=doc.createElement("cputune")
    shares=doc.createElement("shares")
    node=doc.createTextNode(s["shares"])
    shares.appendChild(node)
    cputune.appendChild(shares)
    
    domain.appendChild(cputune)
    
    #os
    os=doc.createElement("os")
    type=doc.createElement("type")
    node=doc.createTextNode("exe") 
    type.appendChild(node)
    os.appendChild(type)
    
    init=doc.createElement("init")
    node=doc.createTextNode("/bin/sh") 
    init.appendChild(node)
    os.appendChild(init)
    
    domain.appendChild(os)
    
    #clock
    clock=doc.createElement("clock")
    clock.setAttribute("offset", "utc")
    domain.appendChild(clock)
    
    #on_poweroff,on_reboot,on_crash
    on_poweroff=doc.createElement("on_poweroff")
    node=doc.createTextNode("destroy") 
    on_poweroff.appendChild(node)
    domain.appendChild(on_poweroff)
    
    on_reboot=doc.createElement("on_reboot")
    node=doc.createTextNode("restart")
    on_reboot.appendChild(node)
    domain.appendChild(on_reboot)
    
    on_crash=doc.createElement("on_crash")
    node=doc.createTextNode("destroy")
    on_crash.appendChild(node)
    domain.appendChild(on_crash)
    
    #devices
    devices=doc.createElement("devices")
    
    console=doc.createElement("console")
    console.setAttribute("type", "pty")
    devices.appendChild(console)
    
    emulator=doc.createElement("emulator")
    node=doc.createTextNode("/usr/lib/libvirt/libvirt_lxc")
    emulator.appendChild(node)
    devices.appendChild(emulator)
    
    #2 network types are provided
    interface=doc.createElement("interface")
    if s["nettype"]=="default":
        interface.setAttribute("type", "network")
    else:
        interface.setAttribute("type", s["nettype"])
    source=doc.createElement("source")
    source.setAttribute("network", s["netlink"])
    interface.appendChild(source)
    devices.appendChild(interface)
    
    domain.appendChild(devices)
    
    
    #Generate XML file
    path="./static/xmls/"+s["name"]+".xml"
    f = open(path,'w')
    f.write(doc.toprettyxml(indent =''))
    f.close()   
    return doc




def newCon(s,user):
    """
    New the container with a setting file "s"
    """
    doc=genXML(s)
    conn=viewCon.getConn();
    name=s["name"]
    path="./static/xmls/"+name+".xml"
    if not os.path.isfile(path):
        return False
    else:
        #Define
        xmlStr=(open(path,'r').read())
        conn.defineXML(xmlStr)
        #Update the database
        dbConn=MySQLdb.connect(host="localhost",user="root",passwd="12345",db="test",charset="utf8")
        cursor=dbConn.cursor()
        t=time.strftime('%Y/%m/%d %H:%M',time.localtime(time.time()))
        sql="insert into LXC_tb values(%s,%s,%s)"
        cursor.execute(sql,[name,user,t])
        dbConn.commit()
        cursor.close()
        conn.close()
    return True

