# -*- coding: utf-8 -*-
import requests
import base64
import re
import urllib
import rsa
import json
import binascii
import MySQLdb

class Userlogin:
  def userlogin(self,username,password,pagecount):
    session = requests.Session()
    url_prelogin = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.5)&_=1364875106625'
    url_login = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'

    #get servertime,nonce, pubkey,rsakv
    resp = session.get(url_prelogin)
    json_data  = re.search('\((.*)\)', resp.content).group(1)
    data       = json.loads(json_data)
    servertime = data['servertime']
    nonce      = data['nonce']
    pubkey     = data['pubkey']
    rsakv      = data['rsakv']

    # calculate su
    su  = base64.b64encode(urllib.quote(username))

    #calculate sp
    rsaPublickey= int(pubkey,16)
    key = rsa.PublicKey(rsaPublickey,65537)
    message = str(servertime) +'\t' + str(nonce) + '\n' + str(password)
    sp = binascii.b2a_hex(rsa.encrypt(message,key))
    postdata = {
      'entry': 'weibo',
      'gateway': '1',
      'from': '',
      'savestate': '7',
      'userticket': '1',
      'ssosimplelogin': '1',
      'vsnf': '1',
      'vsnval': '',
      'su': su,
      'service': 'miniblog',
      'servertime': servertime,
      'nonce': nonce,
      'pwencode': 'rsa2',
      'sp': sp,
      'encoding': 'UTF-8',
      'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
      'returntype': 'META',
      'rsakv' : rsakv,
    }
    resp = session.post(url_login,data=postdata)
    # print resp.headers
    login_url = re.findall('replace\(\'(.*)\'\)',resp.content)
    #
    respo = session.get(login_url[0])
    uid = re.findall('"uniqueid":"(\d+)",',respo.content)[0]
    url = "http://weibo.com/u/"+uid
    respo = session.get(url)
    # print respo.content #获取首页的内容html
    #以上为成功登陆微博

    #获取数据库连接
    conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='weiboanalysis',charset='utf8')
    curs = conn.cursor()
    curs.execute('delete from outbox')

    myheaders={}
    myheaders['set-cookie'] = resp.headers['set-cookie']


    myheaders['Referer'] = 'http://weibo.com/comment/inbox?leftnav=1&wvr=5'
    # print myheaders

    #以下是开始抓取信息
    for i in range(1,int(pagecount)+1):
        forwardUrl = """http://weibo.com/comment/inbox?topnav=1&wvr=5&f=1&page=%d"""%i
        r = session.post(forwardUrl,headers=myheaders)
        page = r.content
        # print page

        #获取并过滤出用户名，存在pagename数组
        pagename = re.findall('<a\s*title=[^>]*usercard[^>]*>',page)
    for n in range(0,len(pagename)):
        pagename[n] = pagename[n].split('\\"')[1]

        #获取并过滤出评论时间，存在pagetime数组
        pagetime = re.findall('WB_time S_func2[^>]*>[^>]*>',page)
    for t in range(0,len(pagetime)):
        pagetime[t] = pagetime[t].split('>')[1].split('<')[0]

        #获取并过滤出评论内容，存在pagecont数组
        pagecont={}
        pagecontent = re.findall(r'<p class=\\\"detail\\(.*?)<\\\/p>',page)
    for t in range(0,len(pagecontent)):
          a = pagecontent[t].split("<\/a>")
          b = a[len(a)-1]
          c = re.sub(r"<img(.*?)>",'[表情]',b) #去掉图片表情
          d = re.sub(r"<span(.*?)span>",'',c)
          pagecont[t] = re.sub(r"\\t|:|：",'',d)  #去掉最后的/t和最前的冒号

    for index in range(0,len(pagetime)):
      sql = """ insert into outbox(uname,time,text) values('%s','%s','%s')"""%(pagename[index],pagetime[index],pagecont[index])
      curs.execute(sql)


    conn.commit()
    curs.close()
    conn.close()