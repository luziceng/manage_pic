# -*- coding:utf-8 -*-
# __author__ = 'cheng'
from srvframe.base import LoginBaseHandler
from dbmanager import manage_pic_db
class UpdateGameHandler(LoginBaseHandler):

    def get(self, *args, **kwargs):
        user_id=self.user["id"]
        menu_id=self.get_argument("menu_id", None)
        if menu_id is None :
            return  self.render("404.html")
        sql="select name from menu where id=%s and user_id =%s and status=0"
        t1=manage_pic_db.get(sql, menu_id, user_id)
        if t1 is []:
            return self.render("404.html")
        sql="select id , game_id from menu_game where menu_id=%s and user_id=%s and status=0"
        menu_name=t1["name"]

        old_game=manage_pic_db.query(sql, menu_id, user_id)
        if old_game is not None:
            for t in old_game:
                sql="select game_name from game where id=%s"
                t["name"]=manage_pic_db.get(sql, t["game_id"])["game_name"]
        sql="select id, game_name from game where status=0"
        games=manage_pic_db.query(sql)
        print games
        self.render("update_game.html", menu_name=menu_name, menu_id=menu_id, old_game=old_game, games=games, user=self.user)

    def post(self, *args, **kwargs):
        new_game=self.get_arguments("new_game")
        menu_id=self.get_argument("menu_id")
        sql = "select name from menu where id=%s and user_id=%s and status=0"
        t=manage_pic_db.get(sql, menu_id, self.user["id"])
        if t is None:
            return self.render("404.html")
        for new in new_game:
            id=new
            if manage_pic_db.get("select game_name from game where id=%s and status=0",id) is None:
                return self.render("404.html")
        sql="update menu_game set status=1 where menu_id=%s and user_id=%s"
        manage_pic_db.execute(sql, menu_id, self.user["id"])
        for new in new_game:
            sql="insert into menu_game (game_id, menu_id , user_id, status) values(%s, %s, %s,%s)"
            manage_pic_db.execute(sql,new, menu_id, self.user["id"], 0)
        sql="insert into log (ids, type, content, operator_id, created_at, admin) values(%s, %s, %s, %s, now(), 0)"
        ids=u"%s"%menu_id
        content=u"%s更新了%s菜单对应的游戏"%(self.user["username"],t["name"])
        manage_pic_db.execute(sql, ids, 5, content, self.user["id"])
        self.redirect("/menu")


class GameHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id=self.user["id"]
        sql="select "