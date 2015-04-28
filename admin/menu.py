#coding: utf-8
__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import manage_pic_db,RedisClient


class CheckMenuHandler(LoginBaseHandler):
    def get(self):#每次从reids取出一个待审核的menu_id
        if RedisClient.llen("menu_under_check") ==0:
            sql="select id from menu where status=2 order by created_at limit 0, 10"
            tt=manage_pic_db.query(sql)
            if tt != []:
                for t in tt:
                    RedisClient.rpush("menu_under_check", t["id"])
        if RedisClient.llen("menu_under_check") ==0:
            return self.render("check_menu.html", res=[], user=self.user)

        sql="select id, name, introduction, pic, user_id from menu where id=%s"
        res = manage_pic_db.query(sql, RedisClient.blpop("menu_under_check"))
        path="/static/pic/dish/"
        for r in res:
            r["pic"]=path+r["pic"]
        self.render("check_menu.html", res=res, user=self.user)



        '''def get(self):#使用redis 存储待审核user_id  每次从redis选一个出来,放到前端
        count=RedisClient.llen("user_under_check")
        if count ==0:
            sql="select id from ordinary_user where status=2 order by created_at  limit 0, 10"
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
        self.render("check_user.html", res=res, user=self.user)'''

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


        self.redirect("/menu")

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
        self.redirect("/menu")



