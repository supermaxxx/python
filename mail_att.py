#!/usr/bin/env python
#encoding=utf-8

import sys
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

# Which below is need to be modified.
MAIL_HOST = 'smtp.??.com'    # smtp server, eg: smtp.qq.com
MAIL_USERNAME = '??????@??.com'    # username of your account, eg: 98***90@qq.com
MAIL_PASSWORD = '??????'    # password of your account
MAIL_TO = '??????@??.com'    # Where to send the mail, eg: 30***04@qq.com
MAIL_SUBJECT = 'This is a python test mail'    # title of the mail

msg = MIMEMultipart()
MAIL_MESSAGE = 'When you see it, the script has run successfully.'  # body of the mail
body = MIMEText(MAIL_MESSAGE)
msg.attach(body)


msg['To'] = MAIL_TO
msg['from'] = MAIL_USERNAME
msg['subject'] = MAIL_SUBJECT

def help():
    print "Useage: eg: python mail_fujian.py /root/soft/123.tgz (with path of the attachment)"
    print "        eg: python mail_fujian.py (without attachment)"


if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            _attachment = sys.argv[1]    # attachment of the mail
            attachment = _attachment.split('/')[-1]
            att = MIMEText(open(_attachment).read(),'base64','gb2312')
            att["Content-Disposition"] = 'attachment;filename="' + attachment + '"'
            msg.attach(att)
        except IOError:
            print "The path to the attachment is not right, exit!"
            help()
            sys.exit(1)
    elif len(sys.argv) < 2:
        pass
    else:
        print "To many argvs, exit!"
        help()
        sys.exit(1)
    try:
        session = smtplib.SMTP()
        session.connect(MAIL_HOST)
        session.login(MAIL_USERNAME,MAIL_PASSWORD)
        session.sendmail(MAIL_USERNAME,MAIL_TO,msg.as_string())
        session.close()
        print 'Success.'
    except Exception,e:
        print e
