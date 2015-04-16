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
        token = self.get_secure_cookie('manage_pic')
        if token in AuthConfig.authed_info:
            self.user={}
            self.user["id"] = AuthConfig.authed_info[token]["id"]
            self.user["username"] = AuthConfig.authed_info[token]["username"]
            self.user["companyname"] = AuthConfig.authed_info[token]["companyname"]
            self.user["email"] = AuthConfig.authed_info[token]["email"]
            self.user["telephone"] = AuthConfig.authed_info[token]["telephone"]
            self.user["license"] = AuthConfig.authed_info[token]["license"]

            return
        self.redirect("/login")

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
        self.render("login.html",msg=None)

    def post(self):
        username=self.get_argument('username','')
        password=self.get_argument('password','')
        sql = "select id, username, password, companyname, telephone, email, license from ordinary_user where username=%s and password=%s and status=0"
        res = manage_pic_db.get(sql, username,password)

        if res is not None:
            key = str(int(random.random() *10**16))
            self.set_secure_cookie('manage_pic',key, expires_days=2)
            AuthConfig.authed_info[key]={}
            AuthConfig.authed_info[key]["id"]=res["id"]
            AuthConfig.authed_info[key]["username"]=res["username"]
            AuthConfig.authed_info[key]["companyname"]=res["companyname"]
            AuthConfig.authed_info[key]["email"]=res["email"]
            AuthConfig.authed_info[key]["telephone"]=res["telephone"]
            AuthConfig.authed_info[key]["license"]=res["license"]
            self.user=res
            self.redirect("/")
        else:
            self.write("用户名或者密码错误")



class LogoutHandler(LoginBaseHandler):
    def get(self):
        token = self.get_secure_cookie('official_msg')
        del AuthConfig.authed_info[token]
        self.clear_cookie('official_msg')
        self.redirect('/login')



