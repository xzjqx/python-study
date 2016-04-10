# -*- coding: utf-8 -*-
import getpass
import urllib
import urllib2

print 'Please input your username: ',
username = raw_input()
# the input of password doesn't echo to console.
userpass = getpass.getpass('Please input your password: ')
values = {
    "username" : username,
    "userpass" : userpass,
    "login" : "Sign In"
}

data = urllib.urlencode(values)
url = "http://acm.hdu.edu.cn/userloginex.php?action=login"
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64)"
headers = { 'User-Agent' : user_agent }

request = urllib2.Request(url,data,headers)
response = urllib2.urlopen(request)

s = response.read().decode('utf-8', 'ignore')
if s.find("No such user or wrong password.") != -1:
    raise Exception ("Login Failed!")
else:
    print 'OK'
#print response.read()
