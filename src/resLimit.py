'''
Created on Apr 17, 2014

@author: wangxingjun
'''

#!/usr/bin/env python  
#coding=utf-8
# from __future__  import division
import viewCon

def getResInfo(con):
    """
    Get the previous resource information
    """
    resInfo={}
    dom=viewCon.getDom(con)
    domInfo=dom.info()
    resInfo["name"]=con
    resInfo["status"]=viewCon.getConInfo(con)["status"]
    resInfo["maxMem"]=domInfo[1]/1024
    resInfo["usedMem"]=domInfo[2]/1024.0
    memtune=dom.memoryParameters(0)
    resInfo["hard_limit"]=memtune["hard_limit"]/1024
    resInfo["swap_hard_limit"]=memtune["swap_hard_limit"]/1024
    resInfo["soft_limit"]=memtune["soft_limit"]/1024
    resInfo["vcpu"]=domInfo[3]
    schedInfo=dom.schedulerParameters()
    resInfo["cpu_shares"]=schedInfo["cpu_shares"]
    return resInfo


def setMem(con,mem):
    """
    Set memory information.
    """
    dom=viewCon.getDom(con)
    maxMem=int(mem["maxMem"])
    preMaxMem=dom.maxMemory()
    if preMaxMem!=maxMem:
        dom.setMaxMemory(maxMem)
    else:
        pass
    
    memParams={}
    memParams["hard_limit"]=mem["hard_limit"]
    memParams["soft_limit"]=mem["soft_limit"]
    memParams["swap_hard_limit"]=mem["swap_hard_limit"]
    preMemParams=dom.memoryParameters(0)
    if preMemParams!=memParams:
        dom.setMemoryParameters(memParams,0)
    else:
        pass
    return None

def setSched(con,sched):
    """
    Set schedule information
    """
    dom=viewCon.getDom(con)
    schedParams=dom.schedulerParameters()
    if schedParams["cpu_shares"]!=sched["cpu_shares"]:
        schedParams["cpu_shares"]=sched["cpu_shares"]
        dom.setSchedulerParameters(schedParams)
    else:
        pass
    dom.setSchedulerParameters(schedParams)
    return None
