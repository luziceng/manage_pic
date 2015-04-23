#!/usr/bin/env python
# -*- coding: utf-8 -*-
#导入smtplib和MIMEText
import smtplib,sys 
from email.mime.text import MIMEText 
def send_mail(sub,content): 

    mailto_list=["294135560@qq.com"]
    mail_host="smtp.163.com"
    mail_user="jslzc1990@163.com"
    mail_pass="jslzc199"
    mail_postfix="gyyx.cn"

    me=mail_user
    msg = MIMEText(content,_charset='gbk')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)
    try:
        s = smtplib.SMTP() 
        s.connect(mail_host) 
        s.login(mail_user,mail_pass) 
        s.sendmail(me, mailto_list, msg.as_string()) 
        s.close() 
        return True
    except Exception, e:
        print str(e)
    return False
if __name__ == '__main__': 
    if send_mail(u'这是python测试邮件',u'python发送邮件'):
        print u'发送成功'
    else:
        print u'发送失败'