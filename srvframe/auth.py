# -*- coding:utf-8 -*-
import urllib
import urllib2
import random
import json

import tornado.ioloop
import tornado.web
from dbmanager import manage_pic_db


class AuthConfig(object):
    duration = 2
    authed_info = {}


class LoginBaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        token = self.get_secure_cookie('admin')
        if token in AuthConfig.authed_info:
            self.user={}
            self.user["id"] = AuthConfig.authed_info[token]["id"]
            self.user["username"] = AuthConfig.authed_info[token]["username"]
            return
        self.redirect("/admin/login")

    def write_error(self,status_code,**kwargs):
        if status_code == 404:
            self.render('404.html')
        else:
            #self.write('error:'+str(status_code))
            self.render('serverError.html')


class LoginHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return manage_pic_db

    def get(self):
        self.render("admin_login.html",msg=None)

    def post(self):
        username=self.get_argument('username','')
        password=self.get_argument('password','')
        sql = "select id, username, password from admin_user where username=%s and password=%s"
        res = manage_pic_db.get(sql, username,password)

        if res is not None:
            key = str(int(random.random() *10**16))
            self.set_secure_cookie('admin',key, expires_days=2)
            AuthConfig.authed_info[key]={}
            AuthConfig.authed_info[key]["id"]=res["id"]
            AuthConfig.authed_info[key]["username"]=res["username"]

            self.user={}
            self.user['id']=res['id']
            self.user['username']=res['username']
            self.redirect("/admin")
        else:
            self.write("用户名或者密码错误")



class LogoutHandler(LoginBaseHandler):
    def get(self):
        token = self.get_secure_cookie('official_msg')
        del AuthConfig.authed_info[token]
        self.clear_cookie('official_msg')
        self.redirect('/login')



