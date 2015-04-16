# -*- coding:utf-8 -*-
__author__ = 'cheng'

import tornado.web
#from srvframe import BaseHandler
from dbmanager import manage_pic_db
import os
import time
from model.register import Register

class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return self.render("login.html")
    def post(self, *args, **kwargs):
        username=self.get_argument("username")
        password=self.get_argument("password")

        sql ="select password from user where username =%s"
        password1=manage_pic_db.get(sql, username)
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
        companyname=self.get_argument('companyname')
        telephone=self.get_argument('telephone')
        email=self.get_argument('email')
        file_metas=self.request.files['license']

        sql ="select id from ordinary_user where username= %s or companyname like %s  or telephone=%s or email=%s"
        t=manage_pic_db.query(sql, username, companyname, telephone, email)
        print t
        if t is  []:
            return self.write("maybe you have already registered, please change your username")



        upload_path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        upload_path=os.path.join(upload_path,'static')
        upload_path=os.path.join(upload_path, 'pic')
        upload_path=os.path.join(upload_path,'license')
        filename=''
        for meta in file_metas:
            filename=meta['filename']
            firstname=filename[:filename.rfind('.')]+str(int(time.time()))
            lastname=filename[filename.rfind('.'):]
            filename=firstname+lastname
            filepath=os.path.join(upload_path, filename)
            with open(filepath,'wb') as up:
                up.write(meta['body'])
        if Register(username, password, companyname,telephone, email, filename).add_user_info():
            self.write("注册信息已经提交,请在两个工作日内检查邮箱邮件，查看注册结果")
        else:
            self.render("serverError.html")






class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return self.write("welcome")
