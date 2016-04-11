#-*-coding:utf8-*-

import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')

if(len(sys.argv) >= 2):
    user_id = (int)(sys.argv[1])
else:
    user_id = (int)(raw_input(u"Input user_id: "))

cookie = {"Cookie": "SUB=_2A2579z6UDeRxGedL7FMQ8i7JyjmIHXVZGELcrDV6PUJbstBeLUfikW1LHes7-yRJaKORxSB-B0mUVhNgZyJC_Q..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5YSnZOAUVwblI6Z3b_2hfs5JpX5o2p; SUHB=0S7DHqH514c-Cn; SSOLoginState=1458785988; gsid_CTandWM=4uyvCpOz5KD2A51daRqP16AIE8j; _T_WM=93274120c8dba7111f46c466c66c40fa"}
url = 'http://weibo.cn/u/%d?filter=1&page=1' % user_id

html = requests.get(url, cookies=cookie).content
selector = etree.HTML(html)
#pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
pageNum = 1

result = ""
urllist_set = set()
word_count = 1
image_count = 1

print u'Spider is ready...'

for page in range(1, pageNum + 1):
    # 获取lxml页面
    url = 'http://weibo.cn/u/%d?filter=1&page=%d' % (user_id, page)
    lxml = requests.get(url, cookies=cookie).content

    # 文字爬取
    selector = etree.HTML(lxml)
    content = selector.xpath('//span[@class="ctt"]')
    for each in content:
        text = each.xpath('string(.)')
        if word_count >= 4:
            text = "%d :" % (word_count - 3) + text + "\n\n"
        else:
            text = text + "\n\n"
        result = result + text
        word_count += 1

    # 图片爬取
    soup = BeautifulSoup(lxml, "lxml")
    urllist = soup.find_all('a', href=re.compile(
        r'^http://weibo.cn/mblog/pic', re.I))
    first = 0
    for imgurl in urllist:
        urllist_set.add(requests.get(imgurl['href'], cookies=cookie).url)
        image_count += 1

fo = open("/mydata/python_test/%s" % user_id, "wb")
fo.write(result)
word_path = os.getcwd() + '/%d' % user_id
print u'Done!!!'

link = ""
fo2 = open("/mydata/python_test/%s_imageurls" % user_id, "wb")
for eachlink in urllist_set:
    link = link + eachlink + "\n"
fo2.write(link)
print u'Image link Done!!!'


if not urllist_set:
    print u'No images'
else:
    # 下载图片,保存在当前目录的pythonimg文件夹下
    image_path = os.getcwd() + '/weibo_image'
    if os.path.exists(image_path) is False:
        os.mkdir(image_path)
    x = 1
    for imgurl in urllist_set:
        temp = image_path + '/%s.jpg' % x
        print u'Downloading %s picture' % x
        try:
            urllib.urlretrieve(urllib2.urlopen(imgurl).geturl(), temp)
        except:
            print u"Failed: %s picture" % imgurl
        x += 1

# print u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count-4,word_path)
# print u'微博图片爬取完毕，共%d张，保存路径%s'%(image_count-1,image_path)
