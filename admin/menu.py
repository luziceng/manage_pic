#coding: utf-8
__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import manage_pic_db,RedisClient


class CheckMenuHandler(LoginBaseHandler):
    def get(self):#每次从reids取出一个待审核的menu_id
        if RedisClient.llen("menu_under_check") ==0:
            sql="select id from menu where status=2 order by created_at limit 0, 10"
            tt=manage_pic_db.query(sql)
            if tt is []:
                return self.render("check_menu.html", res=[], user=self.user)
            for t in tt:
                RedisClient.rpush("menu_under_check")

        sql="select id, name, introduction, pic, user_id from menu where id=%s"
        res = manage_pic_db.query(sql, RedisClient.blpop("menu_under_check"))
        path="/static/pic/dish/"
        for r in res:
            r["pic"]=path+r["pic"]
        self.render("check_menu.html", res=res, user=self.user)

class MenuAcceptHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        menu_id=self.get_argument("menu_id")
        sql="select id from menu where id=%s and status=2"
        t=manage_pic_db.get(sql, menu_id)
        if t==None:
            return  self.render("404.html")
        sql="update menu set status=0 where id=%s"
        manage_pic_db.execute(sql, menu_id)
        sql="update menu_game set status=0 where menu_id=%s"
        manage_pic_db.execute(sql, menu_id)
        sql="update menu_bonus set status=0 where menu_id=%s"
        manage_pic_db.execute(sql, menu_id)


        self.redirect("/admin/menu")

class MenuDeclineHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        menu_id = self.get_argument("menu_id")
        sql="select id from menu where id=%s and status=2"
        t=manage_pic_db.get(sql, menu_id)
        if t==None:
            return  self.render("404.html")
        sql="update menu set status=1 where id=%s"
        manage_pic_db.execute(sql, menu_id)
        sql="update menu_game set status=1 where menu_id=%s"
        manage_pic_db.execute(sql, menu_id)
        sql="update menu_bonus set status=1 where menu_id=%s"
        manage_pic_db.execute(sql, menu_id)
        self.redirect("/admin/menu")



