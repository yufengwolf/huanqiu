# -*- coding: utf-8 -*-
import json,time,re,datetime
from scrapy import Spider
from scrapy import Request,Selector
from sina.util import mysqlObj,myUtil
from sina.items import HTMLItem,CommentItem


class FinanceSpider(Spider):
	"""
67 界面 带jsonp评论
	"""
	name = 'www_jiemian_com'

# 	allowed_domains = list('http://finance.sina.com.cn')

	handle_httpstatus_list = [301, 302]
	sql = mysqlObj()
	connect = sql.connect
	my_kwargs = dict(sumPage=0)
	u = myUtil()
	def start_requests(self):
		"""
		:param settings:
		:return:
		"""
# 		#中国
		yield Request('https://www.jiemian.com/lists/71.html', self.parseList, cb_kwargs=self.my_kwargs)
		yield Request('https://www.jiemian.com/lists/174.html', self.parseList, cb_kwargs=self.my_kwargs)
		yield Request('https://www.jiemian.com/lists/154.html', self.parseList, cb_kwargs=self.my_kwargs)
		yield Request('https://www.jiemian.com/lists/8.html', self.parseList, cb_kwargs=self.my_kwargs)
		yield Request('https://www.jiemian.com/lists/65.html', self.parseList, cb_kwargs=self.my_kwargs)
		yield Request('https://www.jiemian.com/lists/2.html', self.parseList, cb_kwargs=self.my_kwargs)
		yield Request('https://www.jiemian.com/lists/62.html', self.parseList, cb_kwargs=self.my_kwargs)
		yield Request('https://www.jiemian.com/lists/112.html', self.parseList, cb_kwargs=self.my_kwargs)
		yield Request('https://www.jiemian.com/lists/9.html', self.parseList, cb_kwargs=self.my_kwargs)
		
	#解析列表
	def parseList(self, response,sumPage):
		self.sql.request_add_or_update(response.url)
		hasNext = True
		articleList = response.css('div.news-view div.news-right')
		for article in articleList:
			dateStr = article.css('span.date::text').get()
			if dateStr.find('分钟前') != -1:
				dateArticle = datetime.datetime.now() - datetime.timedelta(minutes=60)
			elif dateStr.find('今天') != -1:
				dateArticle = datetime.datetime.now() - datetime.timedelta(hours=12)
			elif dateStr.find('昨天') != -1:
				dateArticle = datetime.datetime.now() - datetime.timedelta(hours=24)
			elif dateStr.find('/') != -1:
				#'03/05 18:56'
				dateArticle = datetime.datetime.strptime(str(self.u.DATEObjectNow.year) + '/' + dateStr, "%Y/%m/%d %H:%M")
			else:
				self.logger.info('checkout unknown date string found in url %s', response.url)
				dateArticle = datetime.datetime.now() - datetime.timedelta(days=60)
				
			if self.u.daysAgo(dateArticle, 3):
				articleInfo = {}
				linkA = response.urljoin(article.xpath('div[@class="news-header"]/h3/a').attrib['href'])	
				commentStr = article.css('span.comment em::text').get(default='0')
				articleInfo['commentCount'] = int(commentStr)
				r = self.sql.request_add(linkA)
				if r != 0 :
					sumPage += 1
					yield response.follow(linkA, self.parseHTML,cb_kwargs=dict(articleInfo=articleInfo))
			else:
				if hasNext:
					self.logger.info('old articles found in url %s', response.url)
				hasNext = False
		
		if sumPage > 100:
			self.logger.info('sum is max at url %s', response.url)
			hasNext = False	
		
		next_page_div = response.xpath('//div[@class="load-more" and contains(text(),"加载更多")]')
		if next_page_div is not None and hasNext :
			next_page_base = next_page_div.attrib['url']
			next_page_page_number = int(next_page_div.attrib['page'])
			next_page_time = str(int(time.time()*1000))
			my_kwargs = dict(next_page_page_number=next_page_page_number,next_page_base=next_page_base,sumPage=sumPage)
			next_page = next_page_base+'&page='+str(next_page_page_number)+'&_='+next_page_time
			self.logger.info('next list url %s', next_page)
			self.sql.request_add(next_page)
			yield response.follow(next_page, callback=self.parseListStep1,cb_kwargs=my_kwargs)
			
	#解析列表
	def parseListStep1(self, response,next_page_page_number,next_page_base,sumPage):
		self.sql.request_add_or_update(response.url)
		hasNext = True
		data = json.loads(response.text[1:-1])
		if 'rst' in data:
			sel = Selector(text=data['rst'], type="html")
			articleList = sel.css('div.news-view div.news-right')
			for article in articleList:				
				dateStr = article.css('span.date::text').get()
				if dateStr.find('分钟前') != -1:
					dateArticle = datetime.datetime.now() - datetime.timedelta(minutes=60)
				elif dateStr.find('今天') != -1:
					dateArticle = datetime.datetime.now() - datetime.timedelta(hours=12)
				elif dateStr.find('昨天') != -1:
					dateArticle = datetime.datetime.now() - datetime.timedelta(hours=24)
				elif dateStr.find('/') != -1:
					#'03/05 18:56'
					dateArticle = datetime.datetime.strptime(str(self.u.DATEObjectNow.year) + '/' + dateStr, "%Y/%m/%d %H:%M")
				else:
					self.logger.info('checkout unknown date string found in url %s', response.url)
					dateArticle = datetime.datetime.now() - datetime.timedelta(days=60)
					
				if self.u.daysAgo(dateArticle, 3):
					articleInfo = {}
					linkA = response.urljoin(article.xpath('div[@class="news-header"]/h3/a').attrib['href'])	
					commentStr = article.css('span.comment em::text').get(default='0')
					articleInfo['commentCount'] = int(commentStr)		
					r = self.sql.request_add(linkA)
					if r != 0 :
						sumPage += 1
						yield response.follow(linkA, self.parseHTML,cb_kwargs=dict(articleInfo=articleInfo))
				else:
					if hasNext:
						self.logger.info('old articles found in url %s', response.url)
					hasNext = False
			
			if sumPage > 100:
				self.logger.info('sum is max at url %s', response.url)
				hasNext = False	
		
			if 'hideLoadBtn' in data and hasNext:
				if (data['hideLoadBtn'] == False) and (int(next_page_page_number) <= 10):
					next_page_page_number = str(int(next_page_page_number)+1)
					next_page_time = str(int(time.time()*1000))
					next_page = next_page_base+'&page='+next_page_page_number+'&_='+next_page_time
					my_kwargs = dict(next_page_page_number=next_page_page_number,next_page_base=next_page_base,sumPage=sumPage)
					self.logger.info('next list url %s', next_page)
					self.sql.request_add(next_page)
					yield response.follow(next_page, callback=self.parseListStep1,cb_kwargs=my_kwargs)

	#全文HTML
	def parseHTML(self, response,articleInfo):	
		item = HTMLItem()	
		item['url'] = response.url
		item['content'] = response
		item['extra'] = articleInfo
		
		articleInfo['read_count'] = None
		aid = re.findall("/(\d+).html", response.url, re.S)
		if len(aid)>0 and len(aid[0])>4:
			infoUrlBase = 'https://a.jiemian.com/index.php?m=article&a=getArticleP&aid='+aid[0]+'&_='+str(int(time.time()*1000))
			try:
				resInfo = self.u.req.get(infoUrlBase,timeout=30)
				infoObj = self.u.myJsonp(resInfo.text)
				hitStr = infoObj['tongjiarr']['hit']
				if hitStr.find('w') != -1:
					hitFloat = float(hitStr[:-1])*10000
					articleInfo['read_count']=int(hitFloat)
				elif hitStr == '':
					articleInfo['read_count']=0
				else:
					try:
						articleInfo['read_count']=int(hitStr)
					except:
						self.logger.info('checkout unkonwn read_count : %s - %s', response.url,hitStr)
			except:
				self.logger.info('checkout unkonwn read_count : %s - %s', response.url,hitStr)
		
		yield item
		
		if articleInfo['commentCount'] > 0:
			if len(aid)>0 and len(aid[0])>4:
				timestampStr = str(int(time.time()*1000))
				pageNo = 1
		# 		linkComment = 'https://a.jiemian.com/index.php?m=comment&a=getlistCommentP&aid=3946385&page=1&comment_type=1&per_page=30&_=1580960089148'
				linkComment = 'https://a.jiemian.com/index.php?m=comment&a=getlistCommentP&aid='+aid[0]+'&page='+str(pageNo)+'&comment_type=1&per_page=30&_='+timestampStr
				yield response.follow(linkComment, self.parseComment,cb_kwargs=dict(articleUrl=response.url,pageNo = pageNo,aid=aid[0]))
		
	#评论
	def parseComment(self, response,articleUrl,pageNo,aid):
		data = self.u.myJsonp(response.text)
		if 'rs' in data:
			sel = Selector(text=data['rs'], type="html")
			commentList = sel.xpath('//dd/div[@class="post-self"]')
			for comment in commentList:
				item = CommentItem()
				item['url'] = articleUrl
				item['author'] = comment.xpath('div[@class="comment-body"]/a/text()').get()
				item['content'] = comment.xpath('div[@class="comment-body"]/div[@class="comment-main"]/p/text()').get()
				item['read_count'] = None
				commentStr = comment.xpath('div[@class="comment-body"]/div[@class="comment-footer"]/span[@class="comment"]//text()').getall()[1]
				item['reply_count'] = int(commentStr[1:-1])
				likeStr = comment.xpath('div[@class="comment-body"]/div[@class="comment-footer"]/span[@class="like"]//text()').getall()[1]
				item['like_count'] = int(likeStr[1:-1])
				#'43分钟前'
				item['issue_time'] = comment.xpath('div[@class="comment-body"]/div[@class="comment-footer"]/span[@class="date"]/text()').get()
				yield item

		if int(data['page_count']) > pageNo:
# 			time.sleep(1)
			timestampStr = str(int(time.time()*1000))
			pageNo = pageNo+1
			linkComment = 'https://a.jiemian.com/index.php?m=comment&a=getlistCommentP&aid='+aid+'&page='+str(pageNo)+'&comment_type=1&per_page=30&_='+timestampStr
			yield response.follow(linkComment, self.parseComment,cb_kwargs=dict(articleUrl=articleUrl,pageNo = pageNo,aid=aid))
			
