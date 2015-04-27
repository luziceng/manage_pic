#coding: utf-8
__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import manage_pic_db
from dbmanager import RedisClient

class AdminHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        self.render("admin.html", username=self.user["username"], user=self.user)

class CheckUserHandler(LoginBaseHandler):
    def get(self):#使用redis 存储待审核user_id  每次从redis选一个出来,放到前端
        count=RedisClient.llen("user_under_check")
        if count ==0:
            sql="select id from ordinary_user where status=2 order by created_at asc limit 0,10"
            res=manage_pic_db.query(sql)
            for r in res:
                RedisClient.rpush("user_under_check", r["id"])
        if RedisClient.llen("user_under_check")==0:
            return self.render("check_user.html", res=[], user=self.user)
        t=RedisClient.blpop("user_under_check")
        sql="select id, username, companyname, telephone, email, license from ordinary_user where id=%s"
        res = manage_pic_db.query(sql,t)
        path="/static/pic/license/"
        for r in res:
            r["license"]=path + r["license"]
        self.render("check_user.html", res=res, user=self.user)

class UserAcceptHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id=self.get_argument("user_id")
        res=manage_pic_db.get("select email ,username  from ordinary_user where id=%s and status=2", user_id)
        if res == None:
            return self.render("404.html")
        user_email=res["email"]
        username=res["name"]
        sql="update ordinary_user set status=0 where id=%s"
        manage_pic_db.execute(sql, user_id)
        from control.mail import SendEmail
        SendEmail(user_email,"%s,恭喜您成功通过本系统的注册，现在您可以登录本系统了"%(username)).sendmail()
        self.redirect("/admin/user")

class UserDeclineHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id = self.get_argument("user_id")
        res=manage_pic_db.get("select email ,username  from ordinary_user where id=% and status=2", user_id)
        if res is None:
            return self.render("404.html")
        user_email=res["email"]
        username=res["name"]
        sql="update ordinary_user set status=1 where id=%s"
        manage_pic_db.execute(sql, user_id)
        from control.mail import SendEmail
        SendEmail(user_email,"%s,很抱歉，您没有通过本系统的审核，请重新检查注册信息，再次提交"%(username)).sendmail()
        self.redirect("/admin/user")



