# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re,datetime,hashlib
from sina.items import PostItem,CommentItem,HTMLItem
from w3lib.html import remove_tags,remove_tags_with_content

class ArticlePipeline(object):
			
	def process_item(self, item, spider):
		"""

		:param item:
		:param spider:
		:return:
		"""
		currentDT = datetime.datetime.now()
		currentDTStr = currentDT.strftime("%Y-%m-%d %H:%M:%S")
		
		#readcount https://a.jiemian.com/index.php?m=article&a=getArticleP&aid=3944646&callback=jQuery110209324970989780061_1580896742496&_=1580896742497
		
		if isinstance(item, HTMLItem):
			
			sele = item.get('content')
			articleInfo = item.get('extra')
			itemP = PostItem()
			
			itemP['url'] = item.get('url')
			spider.logger.info('article: %s', item.get('url'))
			itemP['media_id'] = 67
			itemP['article_id'] = hashlib.md5(item.get('url').encode()).hexdigest()
			itemP['subject'],itemP['issue_time'],itemP['source'],itemP['author'],itemP['body'] = None,None,None,None,None
			itemP['subject'] = sele.xpath('//div[@class="article-view"]/div[@class="article-header"]/h1/text()').get().strip()
	
			try:
				authorList = sele.xpath('//div[@class="person f-cb"]//p//text()').getall()
				if len(authorList) > 0:
					pass
				else:
					authorList = sele.xpath('//div[@class="article-view"]/div[@class="article-info"]/p/span[@class="author"]/a/text()').getall()
				if authorList:
					itemP['author'] = ','.join(authorList)
			except:
				spider.logger.info('get author failed : article: %s', item.get('url'))
				
			infoList = sele.xpath('//div[@class="article-view"]/div[@class="article-info"]/p/span/text()').getall()
			for info in infoList:
				info = remove_tags(info).strip()
				if re.findall("\d{4}/\d{2}/\d{2} \d{2}:\d{2}", info, re.S):
					timeStr = re.findall("\d{4}/\d{2}/\d{2} \d{2}:\d{2}", info, re.S)[0]
					dateObject = datetime.datetime.strptime(timeStr, "%Y/%m/%d %H:%M")
					itemP['issue_time'] = dateObject.strftime("%Y-%m-%d %H:%M:%S")
				elif info.find('来源：') != -1:
					itemP['source'] = info[info.find('来源：')+3:]
				
			contentLists = sele.xpath('//div[@class="article-content"]/*')
			itemP['body'] = ''
			for p in contentLists:
				itemP['body'] += remove_tags(remove_tags_with_content(p.get().strip(), ('style','script'))).strip()+'\n'
			itemP['comment_count'],itemP['read_count'],itemP['forward_count'],itemP['like_count'] = None,None,None,None
			
			itemP['read_count']= articleInfo['read_count']
			itemP['comment_count'] = articleInfo['commentCount']

			itemP['crawl_ip'] = spider.u.myip()
			itemP['crawl_time'] = currentDTStr
	
			return itemP
		elif isinstance(item, CommentItem):
			item['article_id'] = hashlib.md5(item.get('url').encode()).hexdigest()
			
			now = datetime.datetime.now()
			issueTime = now
			relTimeStr = item['issue_time']
			if relTimeStr.find('分钟前') != -1:
				issueTime = now - datetime.timedelta(minutes=int(relTimeStr[:relTimeStr.find('分钟前')]))
			elif relTimeStr.find('小时前') != -1:
				issueTime = now - datetime.timedelta(hours=int(relTimeStr[:relTimeStr.find('小时前')]))
			elif relTimeStr.find('天前') != -1:
				issueTime = now - datetime.timedelta(days=int(relTimeStr[:relTimeStr.find('天前')]))
			elif relTimeStr.find('月前') != -1:
				issueTime = now - datetime.timedelta(days=int(relTimeStr[:relTimeStr.find('月前')])*30)
			else:
				spider.logger.info('get issue_time failed: %s - %s', item.get('url'),relTimeStr)
			item['issue_time'] = issueTime.strftime("%Y-%m-%d %H:%M:%S")
			
			item['crawl_ip'] = spider.u.myip()
			item['crawl_time'] = currentDTStr
			return item
		else:
			return item


