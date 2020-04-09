# -*- coding: utf-8 -*-
import time,datetime,json
from scrapy import Spider
from scrapy import Request
from sina.items import PostItem


class FinanceSpider(Spider):
	"""
此爬虫已废弃，但util中内含公共的pipeline，请勿移除。
	"""
	name = 'sina'

# 	allowed_domains = list('http://finance.sina.com.cn')

	handle_httpstatus_list = [301, 302]
	
	maxPage = 3
	currentPage = 1

	def start_requests(self):
		"""

		:param settings:
		:return:
		"""
		# #         个股点评列表*45
		self.maxPage = 3
		self.currentPage = 1
		yield Request('http://finance.sina.com.cn/roll/index.d.html?cid=56588', self.parseGeGuDianping)

		# #         股票专栏列表(js动态加载)(http://finance.sina.com.cn/zl/stock/)
		self.maxPage = 6
		self.currentPage = 1
		yield Request('https://interface.sina.cn/finance/api_feed.d.json?cid=56461&page=1&size=20', self.parseGupiaoZhuanlan)

		# #         证券深度研究*45
# 		self.maxPage = 3
# 		self.currentPage = 1
# 		yield Request('http://finance.sina.com.cn/roll/index.d.html?lid=1008', self.parseGeGuDianping)

		# #         证券证券原创*45
# 		self.maxPage = 3
# 		self.currentPage = 1
# 		yield Request('http://finance.sina.com.cn/roll/index.d.html?cid=221431', self.parseGeGuDianping)

		#         国内新浪财经(http://finance.sina.com.cn/china/)		
# 		self.maxPage = 6
# 		self.currentPage = 1
# 		yield Request('http://feed.mix.sina.com.cn/api/roll/get?pageid=155&lid=1686&num=20&page=1', self.parseGuonei,meta={'dont_merge_cookies': True})

# #         产经新浪财经http://finance.sina.com.cn/chanjing/	
# 		self.maxPage = 7
# 		self.currentPage = 1
# 		yield Request('http://feed.mix.sina.com.cn/api/roll/get?pageid=164&lid=1693&num=20&page=1', self.parseGuonei,meta={'dont_merge_cookies': True})

		# #         消费新浪财经http://finance.sina.com.cn/consume/	
# 		self.maxPage = 6
# 		self.currentPage = 1
# 		yield Request('http://feed.mix.sina.com.cn/api/roll/get?pageid=166&lid=1703&num=20&page=1', self.parseGuonei,meta={'dont_merge_cookies': True})

		# #         公司研究报告	*40
# 		self.maxPage = 3
# 		self.currentPage = 1
# 		yield Request('http://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/company/index.phtml?p=1', self.parseYanjiuBaogao)

		
		
	#个股点评列表
	def parseGeGuDianping(self, response):
		
		linkList = response.xpath('//ul[@class="list_009"]/li/a')
		for link in linkList:
			yield response.follow(link.attrib['href'], self.parseContentGeGuDianping)
		
		next_page = response.xpath('//table[2]//tbody[1]//tr[1]//td[1]//span[1]//span[7]//a[1]').attrib['href']		
		self.logger.info('next list url %s', next_page)
		if (next_page is not None) and self.currentPage < self.maxPage :
			self.currentPage += 1
			yield response.follow(next_page, callback=self.parseGeGuDianping)
			
	def parseContentGeGuDianping(self, response):
		def extract_with_css(query):
			return response.css(query).get(default='').strip()
		
		def dateStringToTimestamp(s):
			#'%m/%d/%Y %H:%M:%S.%f'
			return time.mktime(datetime.datetime.strptime(s, "%Y年%m月%d日 %H:%M").timetuple())
		
		item = PostItem()
		item['title'] = extract_with_css('h1.main-title::text')
		item['content'] = response.xpath('//div[@id="artibody"]').get().strip()
		item['url'] = response.url
		
		yield item
		
	
		#股票专栏列表(js动态加载)
	def parseGupiaoZhuanlan(self, response):
#		 if len(response.text>0) :
		if len(response.text) > 0 and self.currentPage <= self.maxPage :
			data = json.loads(response.text)
			for article in data['result']['data']['articles']:
				yield response.follow(article['pub_url'], self.parseContentGupiaoZhuanlan)
		
			self.currentPage += 1
			next_page = 'https://interface.sina.cn/finance/api_feed.d.json?cid=56461&page='+str(self.currentPage)+'&size=20'
			self.logger.info('next list url %s', next_page)
			yield response.follow(next_page, callback=self.parseGupiaoZhuanlan)
			
	def parseContentGupiaoZhuanlan(self, response):
		def extract_with_css(query):
			return response.css(query).get(default='').strip()
		
		def dateStringToTimestamp(s):
			#'%m/%d/%Y %H:%M:%S.%f'
			return time.mktime(datetime.datetime.strptime(s, "%Y年%m月%d日 %H:%M").timetuple())

		item = PostItem()
		try:
			item['title'] = ''.join(response.xpath('//h1[@class="main-title"]/text()').extract()).strip()
		except:
			item['title'] = ''.join(response.xpath('//h1[@id="artibodyTitle"]/text()').extract()).strip()
		if item['title'] == '':
			try:
				item['title'] = ''.join(response.xpath('//h1[@id="artibodyTitle"]/text()').extract()).strip()
			except:
				self.logger.error('title not found')
			
		try:
			item['content'] = ''.join(response.xpath('//div[@class="article-content-left"]').extract()).strip()
		except:
			item['content'] = ''.join(response.xpath('//div[@id="artibody"]').extract()).strip()
		if item['content'] == '':
			try:
				item['content'] = ''.join(response.xpath('//div[@id="artibody"]').extract()).strip()
			except:
				self.logger.error('content not found')
			
		item['url'] = response.url
			
		yield item
		
			#国内新浪财经
	def parseGuonei(self, response):
#		 if len(response.text>0) :
		if len(response.text) > 0 and self.currentPage < self.maxPage :
			data = json.loads(response.text)
			for article in data['result']['data']:
				self.logger.info('content url %s', article['url'])
				yield response.follow(article['url'], self.parseContentGupiaoZhuanlan)
		
			self.currentPage += 1
			urlPrefix = response.url[:response.url.find("page=")+5]
			next_page = urlPrefix + str(self.currentPage) + "&_=" + str(int(time.time()*1000))
			self.logger.info('next list url %s', next_page)
			headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
			'Referer':'https://www.sina.com'
			}
			meta = {
			'dont_merge_cookies': True,
			#'proxy': 'http://172.16.2.239:8888'
			}
			yield response.follow(next_page, callback=self.parseGuonei,headers=headers,meta=meta)
			
	#公司研究报告
	def parseYanjiuBaogao(self, response):
		
		linkList = response.xpath('//td[@class="tal f14"]/a')
		for link in linkList:
			yield response.follow(link.attrib['href'], self.parseContentYanjiuBaogao)
		
		nextPageButton = response.xpath('//span[@class="pagebox_next"]/a')
		if (nextPageButton is not None) and (self.currentPage < self.maxPage) :
			self.currentPage += 1
			urlPrefix = response.url[:response.url.find("p=")+2]
			next_page = urlPrefix + str(self.currentPage)
			self.logger.info('next list url %s', next_page)
			yield response.follow(next_page, callback=self.parseYanjiuBaogao)
			
	def parseContentYanjiuBaogao(self, response):
		
		item = PostItem()
		item['title'] = response.xpath('//div[@class="content"]/h1').get().strip()
		item['content'] = response.xpath('//div[@class="blk_container"]').get().strip()
		item['url'] = response.url
		
		yield item
		
			
	#全文HTML
	def parseHTML(self, response):		
		yield {
			'url': response.url,
			'content': response.text,
		}	
		
	def parse(self, response):
		"""

		:param response:
		:return:
		"""
		print(response)
