# -*- coding: utf-8 -*-
import json,time,re,datetime,os
from scrapy import Spider
from scrapy import Request,Selector
from sina.util import mysqlObj
from sina.items import HTMLItem


class FinanceSpider(Spider):
    name = 'finance_huanqiu_com'

    handle_httpstatus_list = [301, 302]
    sql = mysqlObj()
    connect = sql.connect

    def start_requests(self):
        yield Request('https://finance.huanqiu.com/chanjing', self.parse)
        yield Request('https://finance.huanqiu.com/ssgs', self.parse)
        yield Request('https://finance.huanqiu.com/observation', self.parse)
        yield Request('https://finance.huanqiu.com/jinr', self.parse)
        yield Request('https://finance.huanqiu.com/captial', self.parse)

    def parse(self, response):
        self.sql.request_add_or_update(response.url)
        articleList = response.css('li[class^="list-item"]')
        for article in articleList:
            url = article.css('a::attr(href)').extract_first()
            time = article.css('span.time::text').extract_first()
            date = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
            if datetime.datetime.now() - date < datetime.timedelta(days=3):
                r = self.sql.request_add('https://finance.huanqiu.com' + url)
                if r != 0:
                    yield response.follow(url, callback=self.parse_html)
            else:
                self.logger.info('old articles found in url %s', response.url)

    def parse_html(self, response):
        item = HTMLItem()
        item['url'] = response.url
        item['content'] = response
        item['extra'] = None
        yield item