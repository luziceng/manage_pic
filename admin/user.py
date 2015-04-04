__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import manage_pic_db
class AdminHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        self.render("admin.html", username=self.user["username"])

class CheckUserHandler(LoginBaseHandler):
    def get(self):
        sql="select id, username, companyname, telephone, email, license from ordinary_user where status=2"
        res = manage_pic_db.query(sql)
        self.render("check_user.html", res=res)

class UserAcceptHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id=self.get_argument("user_id")
        sql="update ordinary_user set status=0 where user_id=%s"
        manage_pic_db.execute(sql, user_id)
        self.redirect("/admin/user")

class UserDeclineHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id = self.get_argument("user_id")
        sql="update orfinary_user set status=1 where user_id=%s"
        manage_pic_db.execute(sql, user_id)
        self.redirect("/admin/user")



