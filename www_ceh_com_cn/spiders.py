# -*- coding: utf-8 -*-
import json,time,re,datetime,os
from scrapy import Spider
from scrapy import Request,Selector
from sina.util import mysqlObj
from sina.items import HTMLItem

class FinanceSpider(Spider):
    name = 'www_ceh_com_cn'

    handle_httpstatus_list = [301, 302]
    sql = mysqlObj()
    connect = sql.connect
    my_kwargs = dict(sumPage=2)

    def start_requests(self):
        yield Request('http://www.ceh.com.cn/jryw/index.shtml', self.parse, cb_kwargs=self.my_kwargs)
        yield Request('http://www.ceh.com.cn/llpd/index.shtml', self.parse, cb_kwargs=self.my_kwargs)
        yield Request('http://www.ceh.com.cn/cjpd/index.shtml', self.parse, cb_kwargs=self.my_kwargs)

    def parse(self, response, sumPage):
        self.sql.request_add_or_update(response.url)
        hasNext = True
        articleList = response.css('td.jryw_list1')
        for article in articleList:
            url = article.css('a::attr(href)').get()
            time = article.css('span::text').get().split()[0]
            #print(url, time)
            date = datetime.datetime.strptime(time, "%Y-%m-%d")
            if datetime.datetime.now() - date < datetime.timedelta(days=3):
                r = self.sql.request_add('http://www.ceh.com.cn' + url[2:])
                if r != 0:
                    yield response.follow(url, callback=self.parse_html)
            else:
                if hasNext:
                    self.logger.info('old articles found in url %s', response.url)
                hasNext = False

        if sumPage > 30:
            self.logger.info('sum is max at url %s', response.url)
            hasNext = False 
        next_url = os.path.dirname(response.url) + '/index_%s.shtml'%sumPage
        if hasNext:
            sumPage += 1
            my_kwargs = dict(sumPage=sumPage)
            self.logger.info('next list url %s', next_url)
            self.sql.request_add(next_url)
            yield response.follow(next_url, callback=self.parse, cb_kwargs=my_kwargs)

    def parse_html(self, response):
        item = HTMLItem()
        item['url'] = response.url
        item['content'] = response
        item['extra'] = None
        yield item
