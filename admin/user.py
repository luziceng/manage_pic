#coding: utf-8
__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import manage_pic_db
class AdminHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        self.render("admin.html", username=self.user["username"], user=self.user)

class CheckUserHandler(LoginBaseHandler):
    def get(self):
        sql="select id, username, companyname, telephone, email, license from ordinary_user where status=2"
        res = manage_pic_db.query(sql)
        path="/static/pic/license/"
        for r in res:
            r["license"]=path + r["license"]
        self.render("check_user.html", res=res, user=self.user)

class UserAcceptHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id=self.get_argument("user_id")
        user_email=manage_pic_db.get("select email from ordinary_user where id=%s", user_id)["email"]
        sql="update ordinary_user set status=0 where id=%s"
        manage_pic_db.execute(sql, user_id)
        from control.mail import SendEmail
        SendEmail(user_email,"恭喜您成功通过本系统的注册，现在您可以登录本系统了")
        self.redirect("/admin/user")

class UserDeclineHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id = self.get_argument("user_id")
        user_email=manage_pic_db.get("select email from ordinary_user where id=%s", user_id)["email"]

        sql="update ordinary_user set status=1 where id=%s"
        manage_pic_db.execute(sql, user_id)
        from control.mail import SendEmail
        SendEmail(user_email,"很抱歉，您没有通过本系统的审核，请重新检查注册信息，再次提交")
        self.redirect("/admin/user")



