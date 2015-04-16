# -*- coding:utf-8 -*-
__author__ = 'cheng'
from dbmanager import manage_pic_db

class Register():
    def __init__(self, username, password, companyname, telephone, email, license1):
        self.username=username
        self.password=password
        self.companyname=companyname
        self.telephone=telephone
        self.email=email
        self.license=license1

    def add_user_info(self):
        sql="insert into ordinary_user (username, password, companyname, telephone, email, license, created_at)" \
            " values(%s, %s, %s, %s, %s, %s, now())"
        try:
            #print manage_pic_db
            sql1="select  id from ordinary_user where username= %s"
            a=manage_pic_db.query(sql1, self.username)
            sql2="select id from ordinary_user where companyname=%s"
            b=manage_pic_db.query(sql2, self.companyname)
            print a
            print b
            if a == [] and  b == []:
                manage_pic_db.execute(sql, self.username, self.password, self.companyname, self.telephone, self.email, self.license)
                return  True
            else :
                return False


        except Exception:
            print "wrong"
            return False


def main():
    Register('1','2','3','4','5','6').add_user_info()

if __name__=="__main__":
    main()

