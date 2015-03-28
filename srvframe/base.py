# -*- coding:utf-8 -*-
import urllib
import urllib2
import random
import json

import tornado.ioloop
import tornado.web
from database import manage_pic_db


class AuthConfig(object):
    duration = 2
    authed_info = {}


class LoginBaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        token = self.get_secure_cookie('manager_pic')
        if token in AuthConfig.authed_info:
            self.user = AuthConfig.authed_info[token]['user']
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
        self.render("login.html")

    def post(self):
        username=self.get_argument('username','')
        password=self.get_argument('username','')
        sql = "select id, username, password, companyname, telephone, email, license from user where username=%s"
        res = manage_pic_db.get(sql, username)
        password1 = res.get("password")
        if password1 is not None and password1 == password:
            key = str(int(random.random() *10**16))
            self.set_secure_cookie('manage_pic',key, expires_day=2)
            AuthConfig.authed_info[key]=res







        if repassword is None:
            return self.write("用户名错误")
        elif repassword != password:
            return self.write("密码错误")
        else:
            return self.write("登录成功")

                key = str(int(random.random() * 10**16))
                self.set_secure_cookie('official_msg',key,expires_days=AuthConfig.duration)
                params['user']['type'] = res['type']
                AuthConfig.authed_info.set(key, json.dumps(params))
                AuthConfig.authed_info.expire(key, 3600) # 1小时后超时
                self.redirect("/")
            else:
            	self.render("login1.html",error_msg='用户名或密码错误，请重新登陆.',username=username)
        except Exception as e:
            print "Something wrong with server, please try later.", e


class LogoutHandler(LoginBaseHandler):
    def get(self):
        token = self.get_secure_cookie('official_msg')
        AuthConfig.authed_info.delete(token)
        self.clear_cookie('official_msg')
        self.redirect('/login')


class ErrorHandler(LoginBaseHandler):
    def get(self):
        self.write_error(404)
    def write_error(self,status_code,**kwargs):
        if status_code==404:
            self.render('404.html')
        else:
            self.write('error:'+str(status_code))
