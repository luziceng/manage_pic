#coding:utf-8
__author__ = 'cheng'
#!/usr/bin/env python3
#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from config.const import mail_from , mail_pass, mail_host
from email.header import Header


class SendEmail():
    def __init__(self, send_to, content):
        self.send_to=send_to
        self.content=content
    def sendmail(self):
        print self.content
        msg=MIMEText(_text=self.content, _subtype="plain", _charset="utf-8")

        msg['Subject']=u"菜式推广管理平台"
        msg['From']=u"15972225587@163.com"
        msg['To']=self.send_to
        smtp= smtplib.SMTP()
        smtp.connect(mail_host)
        smtp.login(mail_from, mail_pass)
        smtp.sendmail(mail_from, self.send_to, msg.as_string())
        smtp.quit()


def main():
    s=SendEmail("294135560@qq.com", "恭喜您通过审核，您现在可以使用本系统了")
    s.sendmail()
if __name__=="__main__":
    main()