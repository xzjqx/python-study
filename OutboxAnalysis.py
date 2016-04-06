# -*- encoding:utf-8 -*-
__author__ = 'lanzao'
import MySQLdb

class OutboxAnalysis:

  def getMost(self,num):#查看评论最多的前num个人
    conn =  MySQLdb.connect(host='localhost',user='root',passwd='root',db='weiboanalysis',charset='utf8')
    curs = conn.cursor()
    sql="""
    select uid,uname,count(uname) as count
    from outbox
    group by uname
    order by count(uname) desc
    limit %d;
    """% int(num)
    curs.execute(sql)
    conn.commit()
    print "******************Commented rankings**********************"
    for item in curs.fetchall():
      print item[1]+" ",str(item[2])+"times"
    print "*******************************************************"
    curs.close()
    conn.close()

  def getUser(self,user):#查看某用户评论
    conn =  MySQLdb.connect(host='localhost',user='root',passwd='root',db='weiboanalysis',charset='utf8')
    curs = conn.cursor()
    curs.execute("""select * from outbox where uname='%s'"""%user)
    print "*****************************************"
    for item in curs.fetchall():
      print item[1]+"   ",item[2]+"   ",item[3]
    print "*****************************************"
    curs.close()
    conn.close()