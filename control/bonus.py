# _*_ coding:utf-8 _*_

__author__ = 'cheng'
from srvframe.base import LoginBaseHandler
from dbmanager import manage_pic_db
class BonusHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id=self.user["id"]
        sql="select id, name from menu where user_id=%s and status=0"
        res=manage_pic_db.query(sql, user_id)

        if res is not None:
            for t in res:
                sql="select id, bonus from menu_bonus where menu_id=%s and status=0"
                r=manage_pic_db.get(sql, t["id"])
                if r is not None:
                    t['bonus']=r["bonus"]
                    t['bonus_id']=r["id"]
        #print res
        self.render("bonus.html", res=res, user=self.user)


class UpdateBonusHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        bonus_id=self.get_argument("bonus_id",None)
        bonus=self.get_argument("bonus",None)
        menu_id=self.get_argument("menu_id", None)
        menu_name=self.get_argument("menu_name", None)
        if bonus_id is None or bonus is None or menu_id is None or menu_name is None:
            self.write("参数错误")
        return self.render("update_bonus.html", bonus=bonus, bonus_id=bonus_id, menu_id=menu_id, menu_name=menu_name, user=self.user)
    def post(self):
        bonus_id=self.get_argument("bonus_id")
        menu_id=self.get_argument("menu_id")
        new_bonus=float(self.get_argument("new_bonus"))
        sql1="select menu_bonus where id=%s and menu_id=%s and user_id=%s"
        t=manage_pic_db.get(sql1, bonus_id, menu_id, self.user["id"])
        if t is None:
            return self.render("404.html")
        sql="update menu_bonus set bonus=%s where id=%s and menu_id=%s"
        manage_pic_db.execute(sql, new_bonus, bonus_id, menu_id)
        self.redirect("/bonus")

