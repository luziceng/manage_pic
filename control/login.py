__author__ = 'cheng'

import tornado.web
#from srvframe import BaseHandler
from database import user_db

class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return self.render("login.html")
    def post(self, *args, **kwargs):
        username=self.get_argument("username")
        password=self.get_argument("password")

        sql ="select password from user where username =%s"
        password1=user_db.get(sql, username)
        #print password, password1
        if password1 is None:
            return self.write("no such user")

        elif password1['password'] != password:
            #print password1
            return self.write("wrong password")
        return self.write("login success")


class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render("register.html")

    def post(self):
        username=self.get_argument('username')
        password=self.get_argument('password')
        repassword=self.get_argument('repassword')
        if password != repassword:
            return self.write("two password is not the same")
        sql="select id from user where username= %s"
        id=user_db.get(sql, username)
        if id is not None:
            return self.write("username existed")

        sql="insert into user (username, password) values(%s, %s)"
        user_db.execute(sql, username, password)
        return self.write("success")

class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return self.write("welcome")
