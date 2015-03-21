# -*- coding:utf-8 -*-
import urllib
import urllib2
import random
import json

import tornado.ioloop
import tornado.web



class AuthConfig(object):
    duration = 2
    loginUrl =  "http://www.qiushibaike.com/session.js"
    authed_info = []


class LoginBaseHandler(tornado.web.RequestHandler):


    def prepare(self):
        token = self.get_secure_cookie('official_msg')
        if AuthConfig.authed_info.exists(token):
            temp = AuthConfig.authed_info.get(token)
            temp = json.loads(temp)
            self.user = temp['user']
            AuthConfig.authed_info.expire(token, 3600) # 1小时后超时
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
        return official_msg_db

    def get(self):
        self.render("login.html")

    def post(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        duration = random_str(4)
        postdata = urllib.urlencode(
            {
            "login":username.encode('utf-8'),
            "password":password,
            "remember_me":"checked",
            "duration":duration
            }
        )
        req = urllib2.Request(AuthConfig.loginUrl,postdata,headers=headers)
        try:
            response = urllib2.urlopen(req)
            params = response.read()
            params = json.loads(params)
            #print params
            if "user" in params:
                sql = """select type from public where public_id=%s limit 1"""
                res = self.db.get(sql, params['user']['id'])
                if not res:
                    self.render('login1.html',error_msg='对不起, 您还不是公众号!', username=username)
                    return
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
