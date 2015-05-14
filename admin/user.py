#coding: utf-8
__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import manage_pic_db
from dbmanager import RedisClient
from tornado.options import options
from srvframe.helper import  Page
class IndexHandler(LoginBaseHandler):
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
        res = manage_pic_db.query(sql,int(t[1]))
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
        username=res["username"]
        sql="update ordinary_user set status=0 where id=%s"
        manage_pic_db.execute(sql, user_id)
        from control.mail import SendEmail
        SendEmail(user_email,u"%s,恭喜您成功通过本系统的注册，现在您可以登录本系统了"%username).sendmail()
        ids=u"%s"%user_id
        content=u"%s 审核通过了%s的注册请求"%(self.user["username"], username)
        sql="insert into log (ids, type, content, operator_id, created_at, admin) values(%s, %s,%s, %s,now(), 1)"
        manage_pic_db.execute(sql, ids, 11, content, self.user["id"])
        self.redirect("/user")

class UserDeclineHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id = self.get_argument("user_id")
        res=manage_pic_db.get("select email ,username  from ordinary_user where id=%s and status=2", user_id)
        if res is None:
            return self.render("404.html")
        user_email=res["email"]
        username=res["username"]
        sql="update ordinary_user set status=1 where id=%s"
        manage_pic_db.execute(sql, user_id)
        from control.mail import SendEmail
        SendEmail(user_email,u"%s,很抱歉，您没有通过本系统的审核，请重新检查注册信息，再次提交"%username).sendmail()
        ids=u"%s"%user_id
        content=u"%s 审核拒绝了%s的注册请求"%(self.user["username"], username)
        sql="insert into log (ids, type,content,  operator_id, created_at, admin) values(%s, %s,%s, %s,now(), 1)"
        manage_pic_db.execute(sql, ids, 12, content, self.user["id"])
        self.redirect("/user")


class ShowUserHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        index=int(self.get_argument("page", options.page))
        count=int(self.get_argument("count", options.count))
        username=self.get_argument("user_name",None)
        if username !=None:
            sql="select id, username, company, email , telephone, license, status, created_at from ordinary_user where (status=0 or status=1) and  username=%s order by created_at desc limit %s ,%s"

            res=manage_pic_db.query(sql, username, (index-1)*count, count)
            total=manage_pic_db.get("select count(id) as total from ordinary_user where (status=0 or status=1) and username=%s", username)
        else:
            sql="select id, username, companyname, email, telephone, license, status, created_at from ordinary_user  where status=0 or status=1 order by created_at desc limit %s, %s"
            res=manage_pic_db.query(sql,(index-1)*count, count)
            total=manage_pic_db.get("select count(id) as total from ordinary_user where (status=0 or status=1)")
        for r in res:
            path="/static/pic/license/"
            r["license"]=path+r["license"]


        page=Page(size=count, index=index, rows=total>500 and 500 or total, data=res)
        self.render("show_user.html", page=page, user=self.user)
class UserDetailHandler(LoginBaseHandler):
    def get(self):
        index=int(self.get_argument("page", options.page))
        count=int(self.get_argument("count", options.count))
        user_id=self.get_argument("user_id",None)
        if user_id ==None:
            self.render("404.html")
        sql="select id, username, companyname, email, telephone, license  ,status from ordinary_user where id=%s"
        user_info=manage_pic_db.get(sql,user_id)
        user_info["license"]="/static/pic/license/"+user_info["license"]

        sql="select id, name, introduction, pic  , status, created_at from menu where user_id=%s order by created_at desc limit %s, %s"
        res=manage_pic_db.query(sql, user_id,(index-1)*count, count)
        total=manage_pic_db.get("select count(id) as total from menu where user_id=%s", user_id)["total"]
        for r in res:
            r["pic"]="/static/pic/dish/"+r["pic"]

        page=Page(size=count, index=index, rows=total>500 and 500 or total, data=res )
        self.render("user_detail.html", page=page, user=self.user,user_info=user_info)