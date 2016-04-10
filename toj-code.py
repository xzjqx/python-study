# coding=<utf-8>
import urllib2
import re
import urllib
import codecs
from HTMLParser import HTMLParser

print 'input your username:'
username = raw_input()
print 'input your password:'
password = raw_input()
print 'input your output path'
outputpath = raw_input()


def replace_html(s):
    s = s.replace('&quot;', '"')
    s = s.replace('&amp;', '&')
    s = s.replace('&lt;', '<')
    s = s.replace('&gt;', '>')
    s = s.replace('&nbsp;', ' ')
    return s


def replace_html2(s):
    s = s.replace('\|', ' ')
    #s=s.replace('\/',' ')
    s = s.replace('\\', ' ')
    s = s.replace('\*', ' ')
    s = s.replace('?', ' ')
    s = s.replace('\"', ' ')
    s = s.replace('\<', ' ')
    s = s.replace('\>', ' ')
    return s


class MyHtmlParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.num = 0
        self.info = ''

    def handle_starttag(self, tag, attrs):
        # print tag
        if tag == 'table':
            # print 'in'
            self.num += 1

    def handle_data(self, data):
        # print self.num
        if self.num == 2:
            self.info += data
            self.info += '\n'

req = urllib2.Request('http://acm.tju.edu.cn/toj/user_' + username + '.html')
page = urllib2.urlopen(req).read().decode('utf-8')
data = re.findall('(?<=p\()(\d*)(?=\))', page)

k = 0
start = '9999999'

error = []
while k != len(data):
    id = data[k]
    print 'problem:' + id
    while True:
        ans = 0
        # print 'start:'+start
        req_answer = urllib2.Request(
            'http://acm.tju.edu.cn/toj/status.php?pid=' + id + '&accept=1&start=' + start)
        page_answer = urllib2.urlopen(req_answer).read().decode('utf-8')
        # print page_answer
        me = MyHtmlParser()
        me.feed(page_answer)
        me.close()
        # print me.info
        data_answer = re.findall('.+', me.info)
        i = 0
        while i != len(data_answer):
            # print data_answer[i]

            if data_answer[i] == username:
                # print data_answer[i-7]
                url = 'http://acm.tju.edu.cn/toj/show_code.php'
                par = {
                    'user_id': username,
                    'passwd':  password,
                    'sid':     data_answer[i - 7],
                }
                try:
                    demo = urllib2.Request(url, urllib.urlencode(par))
                    code_html = urllib2.urlopen(demo).read().decode('utf-8')
                    code_html = replace_html(code_html)
                    code = re.findall(
                        '(?<=<pre>)([\s\S]*)(?=</pre>)', code_html)[0]
                    titlereq = urllib2.Request(
                        'http://acm.tju.edu.cn/toj/showp' + id + '.html')
                    titlehtml = urllib2.urlopen(
                        titlereq).read().decode('utf-8', 'ignore')
                    title = re.findall(
                        '(?<=<title>)([\s\S]*?)(?=\|)', titlehtml)[0]
                    print title
                    path = replace_html2(outputpath + title + '.cpp')
                    f = codecs.open(path, 'w', 'utf-8')
                    f.write(code)
                    f.close()
                except Exception, e:
                    print e
                    error.append(id)
                start = '9999999'
                ans = 1
                break
            if data_answer[i] == id:
                start = data_answer[i - 2]
            i += 1
        if ans == 1:
            break
    k += 1
print error
