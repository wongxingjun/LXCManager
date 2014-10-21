'''
Created on Mar 21, 2014

@author: wangxingjun
'''

#!/usr/bin/env python  
# coding=utf-8  

import sys
import MySQLdb
import libvirt


StatusMap={0:"running",
           1:"running",
           2:"running",
           3:"paused",
           4:"shutdown",
           5:"shutdown",
           6:"crashed"
           }


def getConn():
    """
    Get connection to the url "lxc:///"
    """
    try:
        conn=libvirt.open("lxc:///")
    except:
        print "Failed to open connection to the hypervisor"
        sys.exit(1)
    return conn



def getDom(con):
    """
    Get a domain object
    """
    conn=getConn()
    if con not in listCons():
        print "Not found this container"
    else:
        return conn.lookupByName(con)

   
def listCons():
    """
    List all containers including active and inactive ones    
    """
    cons=[]
    cons.extend(listActiveCons())
    cons.extend(listInactiveCons())
    return cons


def listActiveCons():
    """
    List active containers
    """
    conn=getConn()
    cons=[]
    for id in conn.listDomainsID():
        cons.append(conn.lookupByID(id).name())
    return cons


def listInactiveCons():
    """
    List inactive containers
    """
    conn=getConn()
    cons=[]
    for id in conn.listDefinedDomains():
        cons.append(id)
    return cons


def getConInfo(con=None):
    """
    Get simple information of a container by its name
    """
    dom=getDom(con)
    raw=dom.info() 
    print raw 
    info= {"CPU":raw[3],
           "CPUtime":int(raw[4]),
           "maxMem":int(raw[1])/1024,
           "Mem":int(raw[2])/1024,
           "status":StatusMap.get(raw[0],"unknow")
           }
    return info

print getConInfo("lxc1")

def getConStatus(con=None):
    dom=getDom(con)
    raw=dom.info()  
    return StatusMap.get(raw[0],"unknow")


def getConDetail(con=None):
    """
    Get detail information of a container
    """
    detail=getConInfo(con)
    dom=getDom(con)
    OS_type=dom.OSType()
    id=dom.ID()
    detail["os"]=OS_type
    detail["id"]=id
    dbConn=MySQLdb.connect(host="localhost",user="root",passwd="12345",db="test",charset="utf8")
    cursor=dbConn.cursor()
    sql="select * from LXC_tb where Name=%s"
    con_=cursor.execute(sql,con)
    con_=cursor.fetchone()
    cursor.close()
    dbConn.commit()
    dbConn.close()
    detail["name"]=con_[0]
    detail["owner"]=con_[1]
    detail["createTime"]=con_[2]
    return detail



def getNodeInfo():
    """
    Get information of a node
    """
    conn=getConn()
    raw=conn.getInfo()
    info={"cpucores":raw[6],
          "cpumhz":raw[3],
          "cpumodel":str(raw[0]),
          "cpus":raw[2],
          "cputhreads":raw[7],
          "numannodes":raw[4],
          "phymemory":raw[1],
          "sockets":raw[5]
          }
    return info

def getAllCons():
    """
    Get information of all containers
    """
    cons=listCons()
    AllCons=[]
    for con in cons:
        info=[con,getConInfo(con)]
        AllCons.append(info)
    return AllCons

def getXML(con):
    """
    Get XML file of a container
    """
    dom=getDom(con)
    return dom.XMLDesc(0)


def getList():
    """
    Get a information list of all containers
    """
    cons=getAllCons()
    dbConn=MySQLdb.connect(host="localhost",user="root",passwd="12345",db="test",charset="utf8")
    cursor=dbConn.cursor()
    sql="select * from LXC_tb"
    n=cursor.execute(sql)
    conList=[]
    ownerInfo=cursor.fetchall()
    for owner in ownerInfo:
        _owner=list(owner)
        print _owner
        for con in cons:
            if con[0]==_owner[0]:
                status=con[1]['status']
                _owner.append(status)
                conList.append(_owner)
    return conList
