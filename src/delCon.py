'''
Created on Mar 21, 2014

@author: wangxingjun
'''

#!/usr/bin/env python  
#coding=utf-8 

import viewCon
import MySQLdb

def undefineCon(con=None):
    """
    Undefine a container with the name "con"
    """
    dom=viewCon.getDom(con)
    #Update the database
    dbConn=MySQLdb.connect(host="localhost",user="root",passwd="12345",db="test",charset="utf8")
    cursor=dbConn.cursor()
    sql="delete from LXC_tb where name=%s"   
    cursor.execute(sql,con)
    cursor.close()
    dbConn.commit()
    dbConn.close()
    return dom.undefine()==0 