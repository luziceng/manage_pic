__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import  manage_pic_db
from config.const import opt_type
from tornado.options import options
from srvframe.helper import Page
class LogHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id=self.get_argument("user_id",None)
        type=self.get_argument("opt_type",None)
        res=[]
        admin=self.get_argument("admin",None)
        index=int(self.get_argument("page", options.page))
        count=int(self.get_argument("count", options.count))
        if type !=None:
            type=int(type)
        total=0
        #print user_id == None
        #print type,type == None
        #print type,type ==0
        if admin !=None:
            admin=int(admin)
        if admin ==1:
            if user_id==None and (type==None or type==0):
                sql="select operator_id ,content, type, created_at, admin from log where admin=1 order by created_at desc limit  %s, %s"
                res=manage_pic_db.query(sql,(index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log where admin=1 ")["total"]
                #print res
            elif user_id==None and type!=0 and type!=None:
                sql="select operator_id,content, type, created_at, admin from log where admin=1 and type=%s order by created_at desc limit  %s, %s"
                res=manage_pic_db.query(sql, type,(index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log where admin=1 and type=%s ", type)["total"]
            elif user_id !=None and (type==0 or type==None):
                sql="select operator_id,content, type, created_at ,admin from log where admin=1 and operator_id=%s order by created_at desc limit  %s, %s"
                res=manage_pic_db.query(sql, user_id,(index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log where admin=1 and operator_id=%s ", user_id)["total"]

            elif user_id !=None and type!=0 and type!=None:
                sql="select operator_id,content, type, created_at , admin from log where admin=1 and operator_id=%s and type=%s order by created_at desc limit  %s, %s"
                res=manage_pic_db.query(sql, user_id, type, (index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log where admin=1 and operator_id=%s and type=%s", user_id, type)["total"]

        elif admin==2:
            if user_id==None and (type==None or type==0):
                sql="select operator_id,content, type, created_at, admin from log where admin=0 order by created_at desc  limit  %s, %s"
                res=manage_pic_db.query(sql,(index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log where admin=0 ")["total"]

                #print res
            elif user_id==None and type!=0 and type!=None:
                sql="select operator_id,content, type, created_at, admin from log where admin=0 and type=%s order by created_at desc limit  %s, %s"
                res=manage_pic_db.query(sql, (index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log where admin=0 and type=%s ", type)["total"]

            elif user_id !=None and (type==0 or type==None):
                sql="select operator_id,content, type, created_at ,admin from log where admin=0 and operator_id=%s order by created_at desc limit  %s, %s"
                res=manage_pic_db.query(sql, user_id,(index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log where admin=0 and operator_id=%s ", user_id)["total"]

            elif user_id !=None and type!=0 and type!=None:
                sql="select operator_id,content, type, created_at , admin from log where admin=0 and operator_id=%s and type=%s order by created_at desc limit  %s, %s"
                res=manage_pic_db.query(sql, user_id, type,(index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log where admin=0 and operator_id=%s and type=%s", user_id, type)["total"]

        else:
            if user_id==None and (type==None or type==0):
                sql="select operator_id,content, type, created_at, admin from log  order by created_at desc  limit  %s, %s"
                res=manage_pic_db.query(sql,(index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log  ")["total"]

                #print res
            elif user_id==None and type!=0:
                sql="select operator_id,content, type, created_at, admin from log where  type=%s order by created_at desc limit  %s, %s"
                res=manage_pic_db.query(sql, type,(index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log where type=%s ", type)["total"]

            elif user_id !=None and (type==0 or type==None):
                sql="select operator_id,content, type, created_at ,admin from log where  operator_id=%s order by created_at desc limit  %s, %s"
                res=manage_pic_db.query(sql, user_id, (index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log where operator_id=%s ", user_id)["total"]
            elif user_id !=None and type!=0:
                sql="select operator_id,content, type, created_at , admin from log where  operator_id=%s and type=%s order by created_at desc limit  %s, %s"
                res=manage_pic_db.query(sql, user_id, type,(index-1)*count, count)
                total=manage_pic_db.get("select count(id) as total from log where type=%s and operator_id=%s", type, user_id)["total"]

        if res != []:
            for r in res:
                r["type"]=opt_type[r["type"]]
                operator_id=r["operator_id"]
                admin=r["admin"]
                if int(admin)==1:
                    r["operator"]=manage_pic_db.get("select username from admin_user where id =%s",operator_id)["username"]
                else:
                    r["operator"]=manage_pic_db.get("select username from ordinary_user where id=%s", operator_id)["username"]
        page=Page(size=count, index=index, rows=total>500 and 500 or total, data=res)
        self.render("log.html", page=page, user=self.user)
        #self.render("log.html",res=res, user=self.user)