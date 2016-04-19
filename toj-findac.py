# -*- coding: utf-8 -*-
import getpass
import urllib
import urllib2
import bs4
import os

def getRunId(user_id, sid_url, run_id):
    request = urllib2.Request(sid_url)
    response = urllib2.urlopen(request)
    soup = bs4.BeautifulSoup(response.read(), "lxml")
    tr = soup.select('tr[height="30"]')
    if len(tr) > 0:
        for x in tr:
            run_id.append(x.get_text()[0:7])
            y = (int)(x.get_text()[0:7])
        sid_url = "http://acm.tju.edu.cn/toj/status.php?user=%s&accept=1&start=%d" %(user_id,y-1)
        getRunId(user_id, sid_url, run_id)
    return run_id

print 'Please Input Your Username: ',
user_id = raw_input()
passwd = getpass.getpass('Please Input Your Password: ')
print 'Please Input Your Target Directory: ',
to_dir = raw_input()

#Verify Your Username
print 'Verifying Your Username...',
sid_url = "http://acm.tju.edu.cn/toj/status.php?accept=1&user=%s" % (user_id)
request = urllib2.Request(sid_url)
response = urllib2.urlopen(request)
soup = bs4.BeautifulSoup(response.read(), "lxml")
tr = soup.select('tr[height="30"]')
if len(tr) == 0:
    raise Exception ("No Such User")
else:
    print '\nDone!'
    print 'Finding Your AC Run Id...'
    run_id = getRunId(user_id, sid_url, [])
    print 'Done!'

#Verify Your Password
print 'Verifying Your Password...',
url = "http://acm.tju.edu.cn/toj/show_code.php"
sid = tr[0].get_text()[0:7]
values = {
    "user_id" : user_id,
    "sid" : sid,
    "passwd" : passwd
}
data = urllib.urlencode(values)
request = urllib2.Request(url,data)
response = urllib2.urlopen(request)
s = response.read().decode('utf-8', 'ignore')
if s.find("Password Error!") != -1:
    raise Exception ("Password Error!")
else:
    print 'Done!'

#Verify Your to_dir
if os.path.exists(to_dir) is False:
    os.mkdir(to_dir)

print 'Printing All Your AC Codes...'
for sid in run_id:
    url = "http://acm.tju.edu.cn/toj/show_code.php"
    values = {
        "user_id" : user_id,
        "sid" : sid,
        "passwd" : passwd
    }
    data = urllib.urlencode(values)
    request = urllib2.Request(url,data)
    response = urllib2.urlopen(request)
    soup = bs4.BeautifulSoup(response.read(), "lxml")
    pid = soup.select('a')[8].get_text()
    code = soup.select('pre')[0].get_text().encode('utf-8')
    fo = open(to_dir + '\\' + pid + u'.cpp', "wb")
    fo.write(code)
