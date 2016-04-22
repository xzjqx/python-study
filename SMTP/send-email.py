# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

from_addr = raw_input('From: ')
password = raw_input('Password: ')
to_addr = raw_input('To: ')
smtp_server = raw_input('SMTP server: ')

msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
msg['From'] = _format_addr(u'SMTP测试 <%s>' % from_addr)
msg['To'] = _format_addr(u'测试者 <%s>' % to_addr)
msg['Subject'] = Header(u'来自SMTP的问候……', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
print u'已建立与SMTP服务器的连接'
server.ehlo()
server.starttls()
server.login(from_addr, password)
print u'邮箱登录成功'
server.sendmail(from_addr, [to_addr], msg.as_string())
print u'成功发送邮件'
server.quit()
print u'完成！'
