# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib,re,datetime
from sina.items import HTMLItem,PostItem

class ArticlePipeline(object):
    def process_item(self, item, spider):
        currentDT = datetime.datetime.now()
        currentDTStr = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(item, HTMLItem):
            response = item['content']
            itemP = PostItem()
            itemP['article_id'] = hashlib.md5(item.get('url').encode()).hexdigest()
            itemP['url'] = item['url']
            itemP['subject'] = response.css('div.t-container-title h3::text').get()
            itemP['issue_time'] = response.css('p.time::text').get()
            itemP['author'] = response.css('p.edit-peo::text').get()[3:]
            data = response.css('div.l-con p::text').extract()
            itemP['body'] = '\n'.join(data)
            itemP['crawl_time'] = currentDTStr
            itemP['source'] = response.css('span.source span::text').get()
            if itemP['source'] == None:
            	itemP['source'] = response.css('span.source a::text').get()
            itemP['media_id'],itemP['read_count'],itemP['comment_count'],itemP['forward_count'],itemP['like_count'],itemP['crawl_ip'] = None,None,None,None,None,None
        return itemP
