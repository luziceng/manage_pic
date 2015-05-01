__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import  manage_pic_db
from config.const import opt_type
class LogHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id=self.get_argument("user_id",None)
        type=self.get_argument("opt_type",None)
        res=[]
        admin=self.get_argument("admin",None)
        if type !=None:
            type=int(type)
        #print user_id == None
        #print type,type == None
        #print type,type ==0
        if admin !=None:
            admin=int(admin)
        if admin ==1:
            if user_id==None and (type==None or type==0):
                sql="select operator_id ,content, type, created_at, admin from log where admin=1 order by created_at desc "
                res=manage_pic_db.query(sql)
                #print res
            elif user_id==None and type!=0 and type!=None:
                sql="select operator_id,content, type, created_at, admin from log where admin=1 and type=%s order by created_at desc"
                res=manage_pic_db.query(sql, type)
            elif user_id !=None and (type==0 or type==None):
                sql="select operator_id,content, type, created_at ,admin from log where admin=1 and operator_id=%s order by created_at desc"
                res=manage_pic_db.query(sql, user_id)
            elif user_id !=None and type!=0 and type!=None:
                sql="select operator_id,content, type, created_at , admin from log where admin=1 and operator_id=%s and type=%s order by created_at desc"
                res=manage_pic_db.query(sql, user_id, type)
        elif admin==2:
            if user_id==None and (type==None or type==0):
                sql="select operator_id,content, type, created_at, admin from log where admin=0 order by created_at desc "
                res=manage_pic_db.query(sql)
                #print res
            elif user_id==None and type!=0 and type!=None:
                sql="select operator_id,content, type, created_at, admin from log where admin=0 and type=%s order by created_at desc"
                res=manage_pic_db.query(sql, type)
            elif user_id !=None and (type==0 or type==None):
                sql="select operator_id,content, type, created_at ,admin from log where admin=0 and operator_id=%s order by created_at desc"
                res=manage_pic_db.query(sql, user_id)
            elif user_id !=None and type!=0 and type!=None:
                sql="select operator_id,content, type, created_at , admin from log where admin=0 and operator_id=%s and type=%s order by created_at desc"
                res=manage_pic_db.query(sql, user_id, type)
        else:
            if user_id==None and (type==None or type==0):
                sql="select operator_id,content, type, created_at, admin from log  order by created_at desc "
                res=manage_pic_db.query(sql)
                #print res
            elif user_id==None and type!=0:
                sql="select operator_id,content, type, created_at, admin from log where  type=%s order by created_at desc"
                res=manage_pic_db.query(sql, type)
            elif user_id !=None and (type==0 or type==None):
                sql="select operator_id,content, type, created_at ,admin from log where  operator_id=%s order by created_at desc"
                res=manage_pic_db.query(sql, user_id)
            elif user_id !=None and type!=0:
                sql="select operator_id,content, type, created_at , admin from log where  operator_id=%s and type=%s order by created_at desc"
                res=manage_pic_db.query(sql, user_id, type)
        if res != []:
            for r in res:
                r["type"]=opt_type[r["type"]]
                operator_id=r["operator_id"]
                admin=r["admin"]
                if int(admin)==1:
                    r["operator"]=manage_pic_db.get("select username from admin_user where id =%s",operator_id)["username"]
                else:
                    r["operator"]=manage_pic_db.get("select username from ordinary_user where id=%s", operator_id)["username"]
        self.render("log.html",res=res, user=self.user)