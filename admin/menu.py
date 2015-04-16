__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import manage_pic_db


class CheckMenuHandler(LoginBaseHandler):
    def get(self):
        sql="select id, name, introduction, pic, user_id from menu where status=2"
        res = manage_pic_db.query(sql)
        path="/static/pic/dish/"
        for r in res:
            r["pic"]=path+r["pic"]
        self.render("check_menu.html", res=res)

class MenuAcceptHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        menu_id=self.get_argument("menu_id")
        sql="update menu set status=0 where id=%s"
        manage_pic_db.execute(sql, menu_id)
        self.redirect("/admin/menu")

class MenuDeclineHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        menu_id = self.get_argument("menu_id")
        sql="update menu set status=1 where id=%s"
        manage_pic_db.execute(sql, menu_id)
        self.redirect("/admin/menu")



