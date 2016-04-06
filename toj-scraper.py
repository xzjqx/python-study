#-*-coding:utf8-*-

import requests
import bs4
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

root_url = 'http://acm.tju.edu.cn/toj/'
pageNum = 3000

for page in range(1001,pageNum+1001):
	index_url = root_url + 'showp%d.html'%(page)
	response = requests.get(index_url)
	soup = bs4.BeautifulSoup(response.text,'lxml')

	num = soup.find_all('center')[1].next.get_text()
	title = soup.find_all(color="blue")[1].get_text()
	problem = soup.select('#problem')[0].get_text()

	result = num + title + '\n' + problem
	fo = open("C:\\Users\\xzjqx\\Desktop\\Python\\toj\\problem%d"%page, "wb")
	fo.write(result)


#print result
