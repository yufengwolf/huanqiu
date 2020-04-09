# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib,re,datetime
from sina.items import WwwCehComCnItem,HTMLItem,PostItem

class ArticlePipeline(object):

    def process_item(self, item, spider):
        currentDT = datetime.datetime.now()
        currentDTStr = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(item, HTMLItem):
            response = item['content']
            itemP = PostItem()#WwwCehComCnItem()
            itemP['article_id'] = hashlib.md5(item.get('url').encode()).hexdigest()
            itemP['url'] = item['url']
            itemP['subject'] = response.css('td.title_content::text').get()
            time = response.css('td.date_content::text').get().split()
            itemP['issue_time'] = time[0] + ' ' + time[1]
            info = response.xpath('//td[@align="left" and contains(text(),"作者")]/text()').extract()[0]
            author = re.findall(r'.*【作者：(.+?)】.*',info.replace('\n', ''))
            if len(author) == 0:
                itemP['author'] = None
            else:
                itemP['author'] = author[0]
            data = response.css('td.content3 *::text').extract()
            itemP['body'] = '\n'.join(data)
            itemP['crawl_time'] = currentDTStr
            itemP['media_id'],itemP['read_count'],itemP['comment_count'],itemP['forward_count'],itemP['like_count'],itemP['crawl_ip'],itemP['source'] = None,None,None,None,None,None,None
        return itemP
