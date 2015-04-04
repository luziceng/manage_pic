__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import manage_pic_db


class CheckUserHandler(LoginBaseHandler):
    def get(self):
        sql="select id, name, introduction, pic, user_id from menu where status=2"
        res = manage_pic_db.query(sql)
        self.render("check_menu.html", res=res)

class UserAcceptHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        menu_id=self.get_argument("menu_id")
        sql="update menu set status=0 where id=%s"
        manage_pic_db.execute(sql, menu_id)
        self.redirect("/admin/user")

class UserDeclineHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        menu_id = self.get_argument("menu_id")
        sql="update menu set status=1 where id=%s"
        manage_pic_db.execute(sql, menu_id)
        self.redirect("/admin/user")



