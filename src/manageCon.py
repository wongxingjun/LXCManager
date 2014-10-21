'''
Created on Mar 21, 2014

@author: wangxingjun
'''

#!/usr/bin/env python  
#coding=utf-8  

from viewCon import getDom,listActiveCons,getConStatus

def startCon(con):
    """
    Start a container with the name con
    """
    dom=getDom(con)
    if con in listActiveCons():
        print "Error!The container is already running or paused!"
        return None
    else:
        return dom.create()==0

def shutdownCon(con):
    """
    Shutdown a container with the name con
    """
    dom=getDom(con)
    status=getConStatus(con)
    if con in listActiveCons():
        if status == "paused":
            dom.resume()
            return dom.destroy()==0
        else:
            return dom.destroy()==0
    else:
        print "Error!The container is already shutdown!"
        return None

def suspendCon(con):
    """
    Suspend a container with the name con
    """
    dom=getDom(con)
    if con in listActiveCons():
        return dom.suspend()==0
    else:
        print "The container is not running and it cannot be paused!"
        return None

def resumeCon(con):
    """
    Resume a container with the name con
    """
    dom=getDom(con)
    if con in listActiveCons():
        return dom.resume()==0
    else:
        print "Error!The container is not active !"
        return None

def rebootCon(con):
    """
    Reboot a container with the name con
    """
    if con in listActiveCons():
        shutdownCon(con)
        return startCon(con)==0
    else:
        print "Error!The container is not active!"
        return None

def oper(name,oper):
    """
    Do the operation post by the page
    """
    do={"start":startCon,"shutdown":shutdownCon,"suspend":suspendCon,
          "resume":resumeCon,"reboot":rebootCon}
    do.get(oper)(name)
    return None
