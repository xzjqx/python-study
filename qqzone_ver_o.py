
#-*-coding:utf-8 -*-


import urllib2,urllib,cookielib,re,hashlib,os,tempfile,sys,json,socket,time,random,time
import xml.dom.minidom
import PyV8
from xml.dom.minidom import parse
from PyQt4 import QtGui,QtCore
from threading import Thread
from Queue import Queue
from datetime import datetime
import traceback


reload(sys)
sys.setdefaultencoding('utf8')
#####

'''cookie'''
cookiejar= cookielib.CookieJar()
cookieproc= urllib2.HTTPCookieProcessor(cookiejar)

####
###设置网络超时###
timeout = 15
socket.setdefaulttimeout(timeout)
###get the page of the url
q=Queue()## 多线程的任务队列
NUM=2  ## 线程数
SUM=0###任务总数
####


def get(url, headers=False) :  ##headers 是加入浏览器标头，反‘反爬虫’；
	if headers:
		req=urllib2.Request(url,headers=headers)
	else :
		req=urllib2.Request(url)
	opener=urllib2.build_opener(cookieproc)
	urllib2.install_opener(opener)
	global Max_Num
	Max_Num=10### 下面的循环则是在遇到网络堵塞的时候，多试几次；一般会成功
	for i in range(Max_Num):
		try:
			page=urllib2.urlopen(req,timeout=20).read()
			try:
				page=page.decode('utf-8')
			except:
				page=page.decode('gbk','ignore')
			return page
			break

		except Exception,ex:
			if i<Max_Num-1:
				continue
			else:
				print Exception,ex

def post(url ,postdata,headers=False):


	if headers:
		req=urllib2.Request(url,postdata,headers=headers)
	else :
		req=urllib2.Request(url,postdata)

	opener=urllib2.build_opener(cookieproc)
	urllib2.install_opener(opener)
	for i in range(Max_Num):
		try:
			page=urllib2.urlopen(req).read()
			try:
				page=page.decode('utf-8')
			except:
				page=page.decode('gbk','ignore')
			return page
			break
		except:
			if i<Max_Num-1:
				continue
			else:
				print 'URLError: <urlopen error timed out> All times is failed '


class QQ:
	num			=""
	pwd			=""
	login_sig	=""
	appid		=549000912
	qzreferrer	=""
	vcode 		=""
	very 		=""


## initial
	def __init__(self,num,pwd):
		self.num=num
		self.pwd=pwd



	##get infomation of Login 获取登录前的一些必需参数
	def check(self):
		'''get login_sig'''
		par = {
			'appid'				: self.appid,
			'daid'				: 5,
			'hide_title_bar'	: 1,
			'link_target'		: "blank",
			'low_login'			: 0,
			'no_verifyimg'		: 1,
			'proxy_url'			: "http://qzs.qq.com/qzone/v6/portal/proxy.html",
			'pt_qr_app'			: "手机QQ空间",
			'pt_qr_help_link'	: "http://z.qzone.com/download.html",
			'pt_qr_link'		: "http://z.qzone.com/download.html",
			'pt_qzone_sig'		: 1,
			'qlogin_auto_login'	: 1,
			's_url'				: "http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
			'self_regurl'		: "http://qzs.qq.com/qzone/v6/reg/index.html",
			'style'				: 22,
			'target'			: "self"
		}
		url='http://xui.ptlogin2.qq.com/cgi-bin/xlogin?%s'% urllib.urlencode(par)
		headers={
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
		}
		#print 'hello'
		get(url,headers)
		for x in cookiejar:
			if x.name =='pt_login_sig':
				self.login_sig = x.value
		print len(cookiejar)

		par = {
			'appid'				: self.appid,
			'pt_tea'			: 1,
			'js_type'			: 1,
			'js_ver'			: 10118,
			'pt_vcode'			: 0,
			'login_sig'			: self.login_sig,
			'r'					: 0.547034760704264,
			'regmaster'			: "",
			'u1'				: "http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
			'uin'				: self.num
		}

		url = 'http://check.ptlogin2.qq.com/check?%s' % urllib.urlencode(par)

		headers={
		"User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER"
		}

		li =  re.findall("'([^']+)'", get(url,headers))
		print li


		if len(li) == 5:
			self.flag, self.vcode, self.uin, self.very, _ = li
			return '1'
		if len(li) == 4:
			self.flag, self.vcode, self.uin, _ =li
			return '1'
		else:
			return '0'

	#code if necessary  验证码的问题
	def getCode(self):
		par = {
			'uin'		: self.num,
			'aid'		: self.appid,
			'cap_cd'	: self.vcode
		}
		url = 'http://captcha.qq.com/getimage?%s' % urllib.urlencode(par)

		url +='&0.15277982888524222'
		opener = urllib2.build_opener(cookieproc)
		urllib2.install_opener(opener)
		req = urllib2.Request(url)

		data=urllib2.urlopen(req).read()
		#print data
		tmp = tempfile.mkstemp(suffix='.png')
		os.write(tmp[0], data)
		os.close(tmp[0])
		os.startfile(tmp[1])
		#self.vcode = raw_input("input the code")

	#get password for rsa
	def getPwd(self):
		with PyV8.JSContext() as ctxt:
			func = ctxt.eval(open('RSA.txt').read())
			rsa = ctxt.locals.getEncryption
			t=rsa(self.pwd,self.num,self.vcode)
			return t



	#get a par :gtk 获取参数
	def gtk(self):

		for x in cookiejar:
			#print x.path
			if x.name == "skey":

				hash = 5381;
				for c in x.value:
					hash += (hash << 5) + ord(c)
				return hash & 0x7fffffff;

	##login the Qzone 模拟登陆
	def login(self):
		print self.vcode
		#print self.very
		par = {
			'u'						: self.num,
			'verifycode'			: self.vcode,
			'pt_vcode_v1'			: 0,
			'pt_verifysession_v1'	: self.very,
			'p'						: self.getPwd(),
			'pt_randsalt'			: 0,
			'u1'					:'http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone',
			'ptredirect'			: 0,
			'h'						: 1,
			't'						: 1,
			'g'						: 1,
			'from_ui'				: 1,
			'ptlang'				: 2052,
			'action'				:'4-36-1428079727760',
			'js_ver'				: 10118,
			'js_type'				: 1,
			'login_sig'				: self.login_sig,
			'pt_uistyle'			: 32,
			'aid'					: 549000912,
			'daid'					: 5,
			'pt_qzone_sig'			: 1
		}
		url = "http://ptlogin2.qq.com/login?%s" % urllib.urlencode(par)

		#print url
		headers={
			'Host'      :'ptlogin2.qq.com',
			'User-Agent': '	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
		}


		res=get(url,headers)
		print res+"++++++++"

		li = re.findall("'([^']+)'", res)
		#print li
		#检验登录信息
		if int(li[0])==0:
			self.qzreferrer = li[2]
			#QtGui.QMessageBox.information(self,'Info','Hello, '+li[len(li) - 1])
			print "你好",li[4]
			return 1
		else:
			#
			return li

	# get all blogs
	def bloglist(self,num,filepath):
			par={
				'absType'					:0,
				'blogType'					:0,
				'cateHex'					:"",
				'cateName'					:"",
				'g_tk'						:self.gtk(),
				'hostUin'					:num,
				'num'						:15,
				'pos'						:0,
				'rand'						:0.7556263920055262,
				'req '                   	:"qzone",
				'reqInfo'					:7,
				'sortType'					:0,
				'source'					:0,
				'statYear'					:2015,
				'uin'						:self.num,
				'verbose'					:1
			}
			url ='http://b1.qzone.qq.com/cgi-bin/blognew/get_abs?%s'%urllib.urlencode(par)
			headers={
				'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER',
				'Host'		:	'b1.qzone.qq.com'
			}

			for i in range(1,Max_Num):
				try:
					data=get(url,headers)
					data 	= data[10:-2]

					data 	= data.replace("\\","")
					obj1 	= json.loads(data.replace('\/','/'),encoding="utf-8")

					totalnum = obj1["data"]["totalNum"]   #get the num of blogs
					page = totalnum/15                    #get the page of html

					page = page+1 if page*15 < totalnum else page

					print "Blog : I come from"+ str(num)


					xml = filepath+'\\'+str(num)+'.xml'
					dom = parse(xml)
					BlogEle = dom.getElementsByTagName('Blog')[0]
					BlogEle.setAttribute('total',str(totalnum))

					f=file(xml,'w')
					dom.writexml(f, addindent=' ',encoding='utf-8')##newl='\n'
					f.close()


					for i in range( 0, page ):

						par["pos"] = 15*(i-1)
						url='http://b11.qzone.qq.com/cgi-bin/blognew/get_abs?%s' %urllib.urlencode(par)
						headers['Host']='b11.qzone.qq.com'
						data=get(url,headers)
						data=data[10:-2]
						data= data.replace("\\","");
						obj1=json.loads(data.replace('\/','/'))
						li=obj1['data']

						if not li.has_key('list'):
							continue;

						for blog in li["list"]:
							self.blog(num,blog['blogId'],filepath)## 进入每一个blog 获取具体信息


				except Exception,e:
					if i<Max_Num-1:
						url='http://user.qzone.qq.com/p/b1/cgi-bin/blognew/get_abs?%s' % urllib.urlencode(par)
						headers['Host']='user.qzone.qq.com'
						continue
					else:
						print Exception,":",e
						traceback.print_exc()
						print "Exception : " +str(num) +' come across a exception in bloglist'


	##具体每个博客的内容
	def blog(self,num,blogid,filepath):
		try:

			par={
				'bdm'								:'b.qzone.qq.com',
				'blogid'							:blogid,
				'dprefix'							:"",
				'imgdm'								:'os.qzs.qq.com',
				'inCharset'							:'utf-8',
				'mode'								:2,
				'numperpage'						:15,
				'outCharset'						:'utf-8',
				'page'								:1,
				'ref'								:'qzone',
				'refererurl'						:'http://cm.qzs.qq.com/qzone/app/blog/v6/bloglist.html#nojump=1&page=1&catalog=list',
				'styledm'							:'cm.qzonestyle.gtimg.cn',
				'timestamp'							:str(time.time())[:-2],
				'uin'								:num

			}
			url='http://b1.qzone.qq.com/cgi-bin/blognew/blog_output_data?%s' %urllib.urlencode(par)
			headers={
				'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER',
				'Host'		:	'b1.qzone.qq.com',
				'Referer'	:	'http://os.qzs.qq.com/qzone/newblog/blogcanvas.html'
				}

			page=str(get(url,headers))
			if not re.search('g_oBlogData',page):
				return

			page = re.search(r'g_oBlogData =  {"data":([\w\W]*?)}};',page).group(1) +'}'
			page = page.replace('\\','').replace('\/','/')
			li 	 = json.loads(page)

			xml=filepath+'\\'+str(num)+'.xml'
			dom =parse(xml)
			f=file(xml,'w')
			BlogListEle=dom.getElementsByTagName('Blog')[0]
			blogEle= dom.createElement('blog')
			BlogListEle.appendChild(blogEle)

			for ele in li:
				if ele == 'comments':
					continue
				if ele == 'pubtime':
					blogEle.setAttribute(ele,datetime.fromtimestamp(li['pubtime']))
				blogEle.setAttribute(ele,str(li[ele]))


			commentListEle=dom.createElement('comments')
			blogEle.appendChild(commentListEle)


			for item in li['comments']:###item is a dict  评论

				qq1=str(item['poster']['id'])
				qq2=str(num)
				commentEle=dom.createElement('comment')
				commentListEle.appendChild(commentEle)

				time_=str(datetime.fromtimestamp(item["postTime"]))
				commentEle.setAttribute('qq1',qq1)
				commentEle.setAttribute('qq2',qq2)
				commentEle.setAttribute('time_rep',time_)
				commentText=dom.createTextNode(item['content'])
				commentEle.appendChild(commentText)

				for rep in item['replies']:
					commentEle=dom.createElement('comment')
					commentListEle.appendChild(commentEle)
					commentEle.setAttribute('qq1',str(rep['poster']['id']))

					content = rep['content']
					if content.find('nick')>-1:
							qq2=content[5:content.index('nick')-1]
							content=content[content.index('}')+1:]
							if qq2[0]==':':
								qq2=qq2[1:]

					else:
						qq2=str(item['poster']['id'])
					posttime=datetime.fromtimestamp(rep['postTime'])
					commentEle.setAttribute('qq2',qq2)
					commentEle.setAttribute('postTime',str(posttime))
					commentText=dom.createTextNode(content)
					commentEle.appendChild(commentText)

			dom.writexml(f, addindent='  ',newl='\n',encoding='utf-8')
			f.close()
		except Exception,ex:
			traceback.print_exc()
			print Exception,ex
			print 'Exception: '+ str(num) + 'met a problem in blog'

	#get the QQ of num  all messages:
	def message(self,num,filepath):
		try:
			print 'Message is starting:'
			par={
				'callback'				:'_preloadCallback',
				'code_version'			:1,
				'format'				:'jsonp',
				'ftype'					:0,
				'g_tk'					:self.gtk(),
				'need_private_comment'	:1,
				'num'					:20,
				'pos'					:0,
				'replynum'				:100,
				'sort'					:0,
				'uin'					:num
			}
			headers={
				'Host'		:	'taotao.qq.com',
				'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
				}
			for i in range(Max_Num):
				url='http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?%s' % urllib.urlencode(par)
				data=get(url,headers)

				data=data[17:-2]
				if data[0]==')':
					data=data[1:-2]
				try:
					data=data.replace('\/','/')
					data=data.replace("\\","");
					obj1=json.loads(data)
					break
				except:
					if i<Max_Num-1:
						continue
					else:
						print 'Exception '+num+' in message come across a json problem'

			xml=filepath+'\\'+str(num)+'.xml'
			## no acess to the qzone for some reason 空间有权限无法进入
			if obj1["code"] != 0:
				os.remove(xml)
				return False

			dom =parse(xml)
			MsgEle=dom.getElementsByTagName('MsgFeeds')[0]



			#print 'Message: I am come from '+ str(num)

			totalnum= obj1["total"]
			print '*****there are %d messages'%int(totalnum)
			MsgEle.setAttribute('total',str(totalnum))
			page= totalnum/20   ##get the page of the webhtml
			if page*20<totalnum:
				page=page+1


			for i in range(1,page+1):
				#print 'Message: I am come from '+ str(num)
				par["pos"]=(i-1)*20
				for i in range(Max_Num):
					url='http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?%s' % urllib.urlencode(par)
					data=get(url,headers)
					data=data[17:-2]
					if data[0]==')':
						data=data[1:-2]
					try:
						data=data.replace('\/','/')
						data=data.replace("\\","")
						obj1=json.loads(data)## json格式
						break
					except:
						if i<Max_Num-1:
							#continue  可能导致重复
							print 'Exception '+num+' in message come across a json problem'
							break
						else:
							print 'Exception '+num+' in message come across a json problem'
							break

				if not obj1.has_key('msglist'):
					continue
				loginID=obj1['logininfo']['uin']
				loginName=obj1['logininfo']['name']
				MsgEle.setAttribute('loginID',str(loginID))
				MsgEle.setAttribute('loginName',str(loginName))

				for message in obj1['msglist']:
					try:
						messageEle=dom.createElement('message')
						MsgEle.appendChild(messageEle)
						createtime=message['created_time']
						time=str(datetime.fromtimestamp(createtime))
						messageEle.setAttribute('time',time)

						lbs=message['lbs']
						placename=str(lbs['idname'])
						pos_x=str(lbs['pos_x'])
						pos_y=str(lbs['pos_y'])

						##手机信息

						messageEle.setAttribute('source_appid',message['source_appid'])
						messageEle.setAttribute('source_name',message['source_name'])
						messageEle.setAttribute('source_url',message['source_url'])
						messageEle.setAttribute('place',placename)
						messageEle.setAttribute('pos_x',pos_x)
						messageEle.setAttribute('pos_y',pos_y)


						##其他信息
						name=message['name']
						rt_sum=message['rt_sum']
						messageEle.setAttribute('name',name)
						messageEle.setAttribute('rt_sum',str(rt_sum))
						total_cmt=str(message['cmtnum'])
						tid = message['tid']
						messageEle.setAttribute('tid',str(tid))
						secret = message['secret']
						messageEle.setAttribute('secret',str(secret))
						##
						##内容
						content=message["content"]
						conEle=dom.createElement('content')
						conText=dom.createTextNode(content)
						messageEle.appendChild(conEle)
						conEle.appendChild(conText)

						##like
						url_like='http://users.qzone.qq.com/cgi-bin/likes/get_like_list_app?%s'%urllib.urlencode(par_like)

						data=str(get(url_like)[10:-3]).replace('\\','')#不能加入headers....！！！！！！！！！！！
						likeinfo=json.loads(data)['data']
						likeEles=dom.createElement('likelists')
						messageEle.appendChild(likeEles)
						for ele in likeinfo:
							if ele=='like_uin_info':
								likerusers = likeinfo[ele]
								for liker in likerusers:
									likeuserEle =dom.createElement('likeuser')
									likeEles.appendChild(likeuserEle)
									likeuserEle.setAttribute(liker,likerusers[liker])
							else:
								likeEles.setAttribute(ele,str(likeinfo[ele]))
					except Exception,e:
						pass

					## 目前最完整的url+par
					par2={
					'format'				:'jsonp',
					'g_tk'					:self.gtk(),
					'hostUin'				:num,
					'inCharset'				:"",
					'need_private_comment'	:1,
					'num'					:20,
					'order'					:0,
					'outCharset'			:"",
					'random'				:0.5869627646619086,
					'ref'					:"",
					'start'					:0,
					'topicId'				:str(num)+'_'+str(tid),
					'uin'					:self.num
					}

					commentlistEle = dom.createElement('comments')
					messageEle.appendChild(commentlistEle)
					total = 0
					for i in range(1,5):
						par2['start']=20*(i-1)
						url='http://taotao.qq.com/cgi-bin/emotion_cgi_getcmtreply_v6?%s' %urllib.urlencode(par2)
						data=str(get(url,headers))
						data=json.loads(data[10:-2])
						#print data.keys()
						data=data["data"]
					 	#print data.keys()
					 	if not data.has_key('comments'):
					 		break
					 	comments=data['comments']
						#print comments
						total += len(comments)
						for comment in comments:## 处理根评论
							qq1=str(comment['poster']['id'])
							qq2=str(num)

							if qq1=="" or qq2=="" or len(qq1)>13 or len(qq2)>13:
								continue
							time_rep=str(datetime.fromtimestamp(comment['postTime']))
							con_rep=str(comment['content'])
							com_id = str(comment['id'])

							commentEle=dom.createElement('comment')
							commentlistEle.appendChild(commentEle)
							commentEle.setAttribute('time_rep',time_rep)
							commentEle.setAttribute('qq1',qq1)
							commentEle.setAttribute('qq2',qq2)
							commentEle.setAttribute('ID',com_id)
							commentEle.setAttribute('platform',str(comment['poster']['platform']))
							commentEle.setAttribute('private',str(comment['private']))


							content_t=dom.createTextNode(con_rep)
							commentEle.appendChild(content_t)

							if not comment.has_key('replies'):
								continue
							replies=comment['replies']##回复评论
							if len(replies)<1:
								continue
							for reply in replies:
								qq1=str(reply['poster']['id'])
								time_rep=str(datetime.fromtimestamp(reply['postTime']))
								content=reply['content']
								if content.find('@{uin')==0:
										qq2=content[5:content.index('nick')-1]
										content=content[content.index('}')+1:]
										if qq2[0]==':':
											qq2=qq2[1:]
								# else:
								# 		qq2=str(item['uin'])
								if qq1=="" or qq2=="" or len(qq1)>13 or len(qq2)>13:
									continue
								rep_id=str(com_id)+'_'+str(reply['id'])
								commentEle=dom.createElement('comment')
								commentlistEle.appendChild(commentEle)
								commentEle.setAttribute('time_rep',time_rep)
								commentEle.setAttribute('qq_1',qq1)
								commentEle.setAttribute('qq_2',qq2)
								commentEle.setAttribute('ID',rep_id)
								commentEle.setAttribute('platform',str(reply['poster']['platform']))
								content_t=dom.createTextNode(content)
								commentEle.appendChild(content_t)

					commentlistEle.setAttribute('total',str(total))



			f=file(xml,'w')
			dom.writexml(f, addindent='  ',newl='\n',encoding='utf-8')##newl='\n'
			f.close()
			#print 	str(num)+'   message is finished'
			return True
		except Exception ,ex:
			traceback.print_exc()
			print Exception , ex
			print 'Exception!' + str(num)+ ' met a problem in message'

	##获得留言板的
	def msgboard(self,num,filepath):
		try:
			par={
			'uin'						:self.num,
			'hostUin'					:num,
			'start'						:0,
			's'							:0.6347675260623405,
			'g_tk'						:self.gtk(),
			'format'					:'jsonp',
			'num'						:10
			}
			url='http://m.qzone.qq.com/cgi-bin/new/get_msgb?%s' % urllib.urlencode(par)
			headers={
				'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER',
				'Host'		:	'm.qzone.qq.com'
				}

			data=get(url,headers)
			data.replace("\\","")
			obj1=json.loads(str(data[10:-2]).replace('\/','/'))

			totalnum=obj1["data"]["total"]
			page=totalnum/10

			if page*10<totalnum:
				page=page+1

			xml=filepath+'\\'+str(num)+'.xml'
			dom =parse(xml)
			MsgBoardEle=dom.getElementsByTagName('MsgBoard')[0]

			MsgBoardEle.setAttribute('total',str(totalnum))


			for i in range(1,page+1):
				#print 'MSgBorard :I am come from '+ str(num)
				par["start"]=10*(i-1)
				url='http://m.qzone.qq.com/cgi-bin/new/get_msgb?%s' % urllib.urlencode(par)
				data=get(url,headers)
				data=data.replace("\\","")
				obj1=json.loads(data[10:-2].replace('\/','/'))
				li = obj1['data']
				if not li.has_key('commentList'):
					continue
				for item in li['commentList']:
					msgboardEle=dom.createElement('message')
					MsgBoardEle.appendChild(msgboardEle)

					for ele in item:

						if ele == 'ubbContent' :

							contentele=dom.createElement("content")
							msgboardEle.appendChild(contentele)
							msgText= dom.createTextNode(str(item[ele]))
							contentele.appendChild(msgText)

						elif not ele == 'replyList':

							msgboardEle.setAttribute(ele, str(item[ele]))


					replylist= item['replyList']

					ReplyEles = dom.createElement("comments")
					msgboardEle.appendChild(ReplyEles)

					if len(replylist) <1:
						continue
					QQ = ''
					if item.has_key('uin'):
						QQ = str(item['uin'])
					for reply in replylist:
						replyele= dom.createElement("comment")
						ReplyEles.appendChild(replyele)
						qq1= str(reply['uin'])
						qq2 =''
						if qq1==QQ:
							qq2=str(num)
						else:
							qq2=QQ
						reply_con=str(reply['content'])
						time_rep=datetime.fromtimestamp(reply['time'])
						replyele.setAttribute("time_rep",str(time_rep))
						replyele.setAttribute("qq1",qq1)
						replyele.setAttribute("qq2",qq2)
						content_ele= dom.createTextNode(reply_con)
						replyele.appendChild(content_ele)


			f=file(xml,'w')
			dom.writexml(f, addindent='  ',encoding='utf-8')##newl='\n'

			f.close()
		except Exception ,ex:
			traceback.print_exc()
			print Exception,ex
			print 'Exception!! '+ str(num)+' in msgboard'
		#print  str(num)+'   MsgBoard is finished'

	##获得朋友列表并且得到其说说，可扩展
	def friendlist(self,filepath):
		par={
			'follow_flag'			:1,
			'groupface_flag'		:0,
			'g_tk'					:self.gtk(),
			'fupdate'				:1,
			'uin'					:self.num
		}

		url='http://r.qzone.qq.com/cgi-bin/tfriend/friend_show_qqfriends.cgi?%s' %urllib.urlencode(par)
		headers={
				'Host'		:	'r.qzone.qq.com',
				'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
			}


		data=get(url,headers)[10:-2].replace('\\','')

		li=json.loads(data)

		print li.keys()#[u'default', u'subcode', u'code', u'data', u'message']
		print 'friendlist :'
		#friend=li["data"]["items_list"][0]
		li=li['data']
		if not li.has_key('items'):
			return
		ownxml=filepath+'\\'+str(self.num)+'_own.xml'
		f=file(ownxml,'w')

		imp1=xml.dom.minidom.getDOMImplementation()
		dom= imp1.createDocument(None,'Qzone',None)
		root =dom.documentElement

		##个人信息
		info=dom.createElement('Info')
		interest=dom.createElement('interests')
		root.appendChild(info)
		root.appendChild(interest)
		par={
				'fupdate'			:1,
				'g_tk'				:self.gtk(),
				'rd'				:0.9476621622250375,
				'uin'				:self.num,
				'vuin'				:self.num
			}
		url='http://base.s8.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?%s' %urllib.urlencode(par)
		headers={
				'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
		}
		infordata=""
		infoli=""
		try:
			infordata=get(url,headers)
			infoli=json.loads(infordata[10:-2].replace('\\','').replace('\/',''))
		except Exception, e:
			url="http://base.edu.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?%s"%urllib.urlencode(par)
			infordata=get(url,headers)
			infoli=json.loads(infordata[10:-2].replace('\\','').replace('\/',''))


		#print infoli
		if infoli['code'] ==0:
			info_data = infoli['data']
			for i in info_data:
				info.setAttribute(str(i),str(info_data[i]))
		else:
			return

		'''
		owner's interest
		'''
		par_inter={
			'flag'			:1,
			'fupdate'		:1,
			'g_tk'			:self.gtk(),
			'rd'			:0.9863470979731075,
			'uin'			:self.num,
			'vuin'			:self.num
		}
		url_inter='http://page.qq.com/cgi-bin/profile/interest_get?%s'%urllib.urlencode(par_inter)
		data=get(url_inter)
		data=data[10:-2].replace('\\','').replace('\/','')
		data=json.loads(data)
		if data.has_key('data'):
			data=data['data']
			for item in data:
				inter_1=data[item]['items']
				for inters in inter_1:
					topic=dom.createElement('Topic')
					topic.setAttribute('flag',str(inters['flag']))
					topic.setAttribute('page',str(inters['page']))
					topic.setAttribute('topic',str(inters['topic']))
					interest.appendChild(topic)

		'''
		interest end
		'''

		'''
		Direct friends
		'''

		friends =dom.createElement('friends')
		friends.setAttribute('frinum',str(len(li['items'])))
		root.appendChild(friends)

		for friend in li['items']:
			q.put(friend)
			friendnode = dom.createElement('friend')
			friends.appendChild(friendnode)
			for ele in friend:
				friendnode.setAttribute(ele,str(friend[ele]))


		'''
		Direct Friends end
		'''

		'''
		UnDirect Friends
		'''
		notfriends=dom.createElement('NotFriends')
		root.appendChild(notfriends)

		gnotfri=dom.createElement('GroupNFri')
		notfriends.appendChild(gnotfri)
		cnotfri=dom.createElement('CircleNFri')
		notfriends.appendChild(cnotfri)
		pnotfriends=dom.createElement('potentialFri')
		notfriends.appendChild(pnotfriends)


		'''
		Group Info
		'''
		par_groups={
		'cntperpage'		:0,
		'fupdate'			:1,
		'g_tk'				:self.gtk(),
		'rd'				:0.9424096878899819,
		'uin'				:self.num
		}
		url='http://r.qzone.qq.com/cgi-bin/tfriend/qqgroupfriend_extend.cgi?%s'%urllib.urlencode(par_groups)
		data=get(url,headers)[10:-2].replace('\\','')
		#print data
		groups=json.loads(data)['data']['group']
		gnotfri.setAttribute('groupnum',str(len(groups)))

		for group in groups:
			groupnode=dom.createElement('group')
			gnotfri.appendChild(groupnode)
			for ele in group:
				groupnode.setAttribute(ele,str(group[ele]))



			groupId = group['groupcode']
			par_group={
			'fupdate'			:1,
			'g_tk'				:self.gtk(),
			'gid'				:groupId,
			'type'				:1,
			'uin'				:self.num
			}

			url='http://r.qzone.qq.com/cgi-bin/tfriend/qqgroupfriend_groupinfo.cgi?%s'%urllib.urlencode(par_group)
			data=get(url,headers)[10:-2].replace('\\','')
			data=json.loads(data)
			friends=data['data']['friends']

			for fri in friends:
				q.put(fri)
				Gfriend=dom.createElement('Gfriend')
				groupnode.appendChild(Gfriend)
				for ele in fri:
					Gfriend.setAttribute(ele,str(fri[ele]))

		'''
		groupfriends end
		'''
		dom.writexml(f, addindent='  ',encoding='utf-8')
		f.close()

		global SUM
		SUM = q.qsize()

		print SUM
		for i in range(NUM):
			t = Thread(target=self.working,args=(filepath,))
			t.setDaemon(True)
			t.setName('Thread -'+ str(i))
			t.start()
		q.join

	##个人信息
	def Info_tab(self,qq1,filepath):
		try:
			xml = filepath +'\\' + qq1+'.xml'
			dom = parse(xml)
			print str(qq1)+' Infomation is starting:'

			InfoEle = dom.getElementsByTagName('Basic')[0]
			interest = dom.getElementsByTagName('Interest')[0]


			'''
			'Basic infor is starting'
			'''

			par={
				'fupdate'			:1,
				'g_tk'				:self.gtk(),
				'rd'				:0.7476621622250375,
				'uin'				:qq1,
				'vuin'				:self.num
			}
			url='http://base.s8.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?%s' %urllib.urlencode(par)
			headers={
				'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER',
				'Host'		:	'base.s8.qzone.qq.com'
				}

			data = get(url,headers)
			infoli = json.loads(data[10:-2].replace('\\','').replace('\/',''))

			if infoli['code'] == 0:
				info_data = infoli['data']
				for i in info_data:
					InfoEle.setAttribute(str(i),str(info_data[i]))

			else:
				return

			'''
			Basic Ends
			'''

			'''
			Intersters is starting
			'''

			par_inter={
			'flag'			:1,
			'fupdate'		:1,
			'g_tk'			:self.gtk(),
			'rd'			:0.9863470979731075,
			'uin'			:qq1,
			'vuin'			:self.num
			}
			url_inter='http://page.qq.com/cgi-bin/profile/interest_get?%s'%urllib.urlencode(par_inter)
			data=get(url_inter)
			data=data[10:-2].replace('\\','').replace('\/','')
			data=json.loads(data)
			if data.has_key('data'):
				data=data['data']
				for item in data:
					inter_1=data[item]['items']
					for inters in inter_1:
						topic=dom.createElement('Topic')
						topic.setAttribute('flag',str(inters['flag']))
						topic.setAttribute('page',str(inters['page']))
						topic.setAttribute('topic',str(inters['topic']))
						interest.appendChild(topic)


			f=file(xml,'w')
			dom.writexml(f, addindent='  ',encoding='utf-8')
			f.close()
		except Exception ,ex:
			traceback.print_exc()
			print Exception,ex
			print 'Exception: in '+ str(qq1)+ 'info_tab'

	#发表说说
	def publish(self,content):
		postdata={
			'code_version'						:1,
			'con'								:content,
			'feedversion'						:1,
			'format'							:'fs',
			'hostuin'							:self.num,
			'paramstr'							:1,
			'pic_template'						:"",
			'qzreferrer'						:'http://user.qzone.qq.com/'+self.num,
			'richtype'							:"",
			'richval'							:"",
			'special_url'						:"",
			'subrichtype'						:"",
			'syn_tweet_verson'					:"",
			'to_sign'							:0,
			'to_tweet'							:0,
			'ugc_right'							:1,
			'ver'								:1,
			'who'								:1
		}
		postdata=urllib.urlencode(postdata)
		url='http://user.qzone.qq.com/q/taotao/cgi-bin/emotion_cgi_publish_v6?g_tk='+str(self.gtk())
		headers={
		'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER',
		'Host'		:	'user.qzone.qq.com'
		}
		post(url,postdata,headers)
		print 'ok'

	def onejob(self,friend,filepath):
		try:
			fuin=''
			fname=''
			if friend.has_key('uin'):
				fuin=str(friend['uin'])
			elif friend.has_key('fuin'):
				fuin=str(friend['fuin'])
			if friend.has_key('name'):
				fname=friend['name']
			elif friend.has_key('nick'):
				fname=friend['nick']
			elif friend.has_key('remark'):
				fname=friend['remark']

			if friend.has_key('groupid'):
				groupid= friend['groupid']
				if groupid==20:
					return

			xmlfile=filepath+'\\'+str(fuin)+'.xml'

			if os.path.exists(xmlfile):
				return
			f=file(xmlfile,'w')

			imp1=xml.dom.minidom.getDOMImplementation()
			dom= imp1.createDocument(None,'Qzone',None)
			root =dom.documentElement


			infoEle =dom.createElement('Info')
			root.appendChild(infoEle)
			info = dom.createElement('Basic')
			infoEle.appendChild(info)
			interst = dom.createElement('Interest')
			infoEle.appendChild(interst)

			MsgEle=dom.createElement('MsgFeeds')
			BlogEle=dom.createElement('Blog')
			msgboardEle=dom.createElement('MsgBoard')
			root.appendChild(MsgEle)
			root.appendChild(BlogEle)
			root.appendChild(msgboardEle)


			s1=str(fuin)+" is starting"

			dom.writexml(f, addindent='  ',encoding='utf-8')
			f.close()

			print 'I am come from '+ str(fuin)
			#self.Info_tab(str(fuin),filepath)
			#self.msgboard(str(fuin),filepath)
			self.bloglist(str(fuin),filepath)
			return
			state=self.message(str(fuin),filepath)


			time.sleep(0.1)
			if state:
				self.Info_tab(str(fuin),filepath)

				time.sleep(0.1)
				self.bloglist(str(fuin),filepath)
				time.sleep(0.1)
				self.msgboard(str(fuin),filepath)
				time.sleep(0.1)



		except Exception,ex:
			traceback.print_exc()
			print 'Exception : ' +str(friend['uin'])
			print Exception,ex
		finally:
			global SUM
			SUM-=1
			s2=str(fuin) + ' is finishing, '+ str(SUM)+' left'
			print s2

	def working(self,filepath):
		while True:
			friend = q.get()
			self.onejob(friend,filepath)
			q.task_done()

class MyDialog(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.setWindowTitle('QZone')
		self.setGeometry(300,300,300,300)


		qq_label=QtGui.QLabel('QQ:',self)
		pwd_label=QtGui.QLabel('PWD',self)
		qq_label.setGeometry(10,10,100,30)
		pwd_label.setGeometry(10,50,100,30)
		code_label= QtGui.QLabel('CODE',self)
		code_label.setGeometry(10,100,100,30)

		self.qq_text=QtGui.QLineEdit(self)
		self.qq_text.setGeometry(40,10,200,30)

		self.pwd_text=QtGui.QLineEdit(self)
		self.pwd_text.setGeometry(40,50,200,30)

		self.pwd_text.setEchoMode( QtGui.QLineEdit.Password )
		self.code_text=QtGui.QLineEdit(self)
		self.code_text.setGeometry(40,100,200,30)



		self.check_btn=QtGui.QPushButton('check',self)
		self.check_btn.setGeometry(20,150,70,40)
		self.login_btn = QtGui.QPushButton('login',self)
		self.login_btn.setGeometry(110,150,70,40)
		self.dir_btn=QtGui.QPushButton('Open',self)
		self.dir_btn.setGeometry(200,150,70,40)
		#self.connect(self.friend_btn,QtCore.SIGNAL('clicked()'),QtGui.qApp,QtCore.SLOT((self.runing())))
		self.check_btn.clicked.connect(self.runing)


	def runing(self):

		num=self.qq_text.text()
		pwd=self.pwd_text.text()

		global qq# 全局变量


		qq = QQ(str(num),str(pwd))
		tag=qq.check()
		if tag=='0':
			QtGui.QMessageBox.information(self,'Erroe','      Please    input    again         ')
			return
		if qq.flag=='1':
			qq.getCode()
			#print self.vcode
			self.login_btn.clicked.connect(self.login_)
		else:
			QtGui.QMessageBox.information(self,'Info','         Login              ')
			self.login_btn.clicked.connect(self.login_)
	def login_(self):
		#num=self.qq_text.text()
		#pwd=self.pwd_text.text()
		global qq
		print "nihao"
		if qq.flag=='1':
			qq.vcode=str(self.code_text.text())
		res = qq.login()
		if res==1:

			global selectDirName
			selectDirName=QtGui.QFileDialog.getExistingDirectory(None,"Select a directory","")
			self.dir_btn.clicked.connect(self.func)
		else:
			QtGui.QMessageBox.information(self,'Info',res[4])

	def func(self):
		print selectDirName
		for root, dis,filess in os.walk(str(selectDirName)):
			for filexml in filess:
					if filexml.find('log.txt'):
						continue;
					filexml=str(selectDirName)+'\\'+filexml
					f=file(filexml,'r').read()
					f=str(f);
					if f.find('<?xml version="1.0"')>-1:
						continue;
					else :
						print filexml + 'has been removed'
						os.remove(filexml)

		qq.friendlist(str(selectDirName))

app =QtGui.QApplication(sys.argv)
myDialog = MyDialog()
myDialog.show()
sys.exit(app.exec_())

