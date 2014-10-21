'''
Created on May 15, 2014

@author: wangxingjun
'''

#!/usr/bin/env python  
#coding=utf-8  

import MySQLdb
import time

def getUserList():
    dbConn=MySQLdb.connect(host="localhost",user="root",passwd="12345",db="test",charset="utf8")
    cursor=dbConn.cursor()
    sql="select * from user_tb"
    n=cursor.execute(sql)
    users=cursor.fetchall()
    userList=[]
    for user in users:
        _user=list(user)
        userList.append(_user)
    return userList

# print getUserList()


def getUserInfo(name):
    userList=getUserList()
    dbConn=MySQLdb.connect(host="localhost",user="root",passwd="12345",db="test",charset="utf8")
    cursor=dbConn.cursor()
    sql="select * from user_tb where username=%s"
    n=cursor.execute(sql,name)
    user=cursor.fetchone()
    return user

def chgUser(username,passwd):
    dbConn=MySQLdb.connect(host="localhost",user="root",passwd="12345",db="test",charset="utf8")
    cursor=dbConn.cursor()
    sql="update user_tb set passwd=%s where username=%s"
    cursor.execute(sql,[passwd,username])
    dbConn.commit()
    cursor.close()
    return True   

# chgUser("wangxingjun","12345")    
    
# print getUserInfo("wangxingjun")

def delUser(name):
    dbConn=MySQLdb.connect(host="localhost",user="root",passwd="12345",db="test",charset="utf8")
    cursor=dbConn.cursor()
    sql="delete from user_tb where username=%s"
    n=cursor.execute(sql,name)
    dbConn.commit()
    cursor.close()
    return True   

def addUser(user):
    dbConn=MySQLdb.connect(host="localhost",user="root",passwd="12345",db="test",charset="utf8")
    cursor=dbConn.cursor()
    sql="insert into user_tb values(%s,%s,%s,%s)"
    t=time.strftime('%Y/%m/%d %H:%M',time.localtime(time.time()))
    n=cursor.execute(sql,[user["username"],user["passwd"],t,user["userType"]])
    dbConn.commit()
    cursor.close()
    return True


def userType(username):
    dbConn=MySQLdb.connect(host="localhost",user="root",passwd="12345",db="test",charset="utf8")
    cursor=dbConn.cursor()   
    sql="select * from user_tb where username=%s and userType=%s" 
    n=cursor.execute(sql,[username,"admin"])
    if n:
        return True
    else:
        return False

def checkUserNotExist(username):
    dbConn=MySQLdb.connect(host="localhost",user="root",passwd="12345",db="test",charset="utf8")
    cursor=dbConn.cursor()   
    sql="select * from user_tb where username=%s"
    n=cursor.execute(sql,username)
    if n:
        return False
    else:
        return True