'''
Created on Mar 20, 2014

@author: wangxingjun
'''

#!/usr/bin/env python  
#coding=utf-8  
import web
import MySQLdb
import getHostInfo
import userMg
import viewCon
import newCon
import delCon
import manageCon
import resLimit

urls=(
     "/","Login",
     "/logout","Logout",
     "/home","Home",
     "/usermg","UserMg",
     "/chguser","ChgUser",
     "/chguser/(\w+)","ChgUserDo",
     "/deluser","DelUser",
     "/deluser/(\w+)","DelUserDo",
     "/adduser","AddUser",
     "/host","Host",
     "/view","View",
     "/detail/(\w+)","Detail",
     "/viewxml/(\w+)","viewXML",
     "/new","New",
     "/del","Delete",
     "/delete/(\w+)","DeleteDo",
     "/manage","Manage",
     "/oper/(\w+)/(\w+)","Operation",
     "/resource/(\w+)","ResourceLimit"
     )

app=web.application(urls,globals())
render=web.template.render("templates/")

class Login:
    def GET(self):
        return render.login()
    def POST(self):
        info=web.input();
        username=info["username"];
        passwd=info["passwd"]
        dbConn=MySQLdb.connect(host="localhost",user="root",
                               passwd="12345",db="test",charset="utf8")
        cursor=dbConn.cursor()
        sql="select * from user_tb where username=%s and passwd=%s"
        params=(username,passwd)
        n=cursor.execute(sql,params) 
        if n:
            web.setcookie("username",username, 3600)
            raise web.seeother("/home")
        else:
            raise web.seeother("/")

class Logout:
    def GET(self):
        web.setcookie("username", "")
        raise web.seeother("/")       
    
class Home():
    def GET(self):
        username=web.cookies().get("username")
        if username:
            return render.home(username)
        else:
            return "Not Found"

class Host():
    def GET(self):
        username=web.cookies().get("username")
        if username:
            hostInfo=getHostInfo.getInfo()
            return render.host(hostInfo,username)
        else:
            return "Not Found" 

class UserMg():
    def GET(self):
        username=web.cookies().get("username")
        if userMg.userType(username):
            return render.usermg(username)
        else:
            raise web.seeother("/home")

class DelUser():
    def GET(self):
        username=web.cookies().get("username")
        if userMg.userType(username):
            userlist=userMg.getUserList()
            return render.userlistDel(userlist,username)
        else:
            return "Not Found"        

class DelUserDo():
    def GET(self,name):
        username=web.cookies().get("username")
        if userMg.userType(username):
            userMg.delUser(name)
            raise web.seeother("/deluser")
        else:
            return "Not Found"

class AddUser():
    def GET(self):
        username=web.cookies().get("username")
        if userMg.userType(username):
            return render.adduser()
        else:
            return "Not Found"
    def POST(self):
        username=web.cookies().get("username")
        if userMg.userType(username):
            data=web.input()
            user={}
            user["username"]=data.get("username")
            user["passwd"]=data.get("passwd")
            user["userType"]="normal"
            if userMg.checkUserNotExist(user["username"]):
                userMg.addUser(user)
            else:
                pass
            raise web.seeother("/usermg")
        else:
            return "Not Found" 

class ChgUser():
    def GET(self):
        username=web.cookies().get("username")
        if username:
            userlist=userMg.getUserList()
            return render.userlistChg(userlist,username)
        else:
            return "Not Found"        

class ChgUserDo():
    def GET(self,name):
        username=web.cookies().get("username")
        if username:
            user=userMg.getUserInfo(name)
            return render.chguser(user)
        else:
            return "Not Found"        
    
    def POST(self,name):
        username=web.cookies().get("username")
        if username:
            data=web.input()
            name=data.get("username")
            newpasswd=data.get("newpasswd")
            userMg.chgUser(name, newpasswd)
            if userMg.userType(username):
                raise web.seeother("/usermg")
            else:
                raise web.seeother("/home")
        else:
            return "Not Found"         

class View():
    def GET(self):
        username=web.cookies().get("username")
        if username:
            conList=viewCon.getList()
            return render.view(conList,username)
        else:
            return "Not Found" 

class Detail():
    def GET(self,name):
        username=web.cookies().get("username")
        if username:
            con=viewCon.getConDetail(name)
            return render.detail(con,username)
        else:
            return "Not Found" 

class viewXML():
    def GET(self,name):
        username=web.cookies().get("username")
        if username:
            return viewCon.getXML(name)
        else:
            return "Not Found" 

class New():
    def GET(self):
        username=web.cookies().get("username")
        if username:
            return render.new(username)
        else:
            return "Not Found" 
    def POST(self):
        username=web.cookies().get("username")
        if username:
            data=web.input()
            setting={}
            setting["name"]=data.get("name")
            setting["maxMem"]=str(int(data["maxMem"])*1024)      
            setting["curMem"]=str(int(data["curMem"])*1024)
            setting["hard_limit"]=str(int(data["hdrMem"])*1024)
            setting["soft_limit"]=str(int(data["sfMem"])*1024)
            setting["swap_hard_limit"]=str(int(data["spMem"])*1024)
            setting["vcpus"]=data["vcpus"]
            setting["shares"]=data["cpushares"]
            setting["nettype"]=data["nettype"]
            setting["netlink"]=data["netlink"]
            newCon.newCon(setting,username)
            raise web.seeother("/view")
        else:
            return "Not Found"
    
class Delete():
    def GET(self):
        username=web.cookies().get("username")
        if username:
            conList=viewCon.getList()
            return render.delete(conList,username)
        else:
            return "Not Found"

class DeleteDo():
    def GET(self,name):
        username=web.cookies().get("username")
        if username:
            delCon.undefineCon(name)
            raise web.seeother("/del")
        else:
            return "Not Found"
      

class Manage():
    def GET(self):
        username=web.cookies().get("username")
        if username:
            conList=viewCon.getList()
            return render.manage(conList,username)
        else:
            return "Not Found"


class Operation():
    def GET(self,name,oper):
        username=web.cookies().get("username")
        if username:
            manageCon.oper(name, oper)
            raise web.seeother("/manage")
        else:
            return "Not Found"
        

class ResourceLimit():
    def GET(self,name):
        username=web.cookies().get("username")
        if username:
            resInfo=resLimit.getResInfo(name)
            return render.res(resInfo,username)
        else:
            return "Not Found"
    def POST(self,name):
        data=web.input()
        mem={}
        mem["maxMem"]=int(data["maxMem"])*1024
        mem["hard_limit"]=int(data["hdrMem"])*1024
        mem["swap_hard_limit"]=int(data["spMem"])*1024
        mem["soft_limit"]=int(data["sfMem"])*1024
        sched={}
        sched["cpu_shares"]=int(data["cpushares"])
        resLimit.setMem(name, mem)
        resLimit.setSched(name, sched)
        raise web.seeother("/manage")
        
        
if __name__=="__main__":
    app.run()
    
        
