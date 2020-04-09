# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class SpiderMiddleware(object):
    """

    """


    def process_spider_input(self, response, spider):
        """

        :param response:
        :param spider:
        :return:
        """
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None


    def process_spider_output(self, response, result, spider):
        """

        :param response:
        :param result:
        :param spider:
        :return:
        """
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for o in result:

            yield o


    def process_spider_exception(self, response, exception, spider):
        """

        :param response:
        :param exception:
        :param spider:
        :return:
        """
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass


    def process_start_requests(self, start_requests, spider):
        """

        :param start_requests:
        :param spider:
        :return:
        """
        for request in start_requests:

            yield request


class DownloaderMiddleware(RetryMiddleware):
    """

    """


    def process_request(self, request, spider):
        """

        :param request:
        :param spider:
        :return:
        """
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # request.meta['proxy'] = 'http://127.0.0.1:8080'
        # if request.url.startswith("http://"):
        #     request.meta['proxy']="http://"+'10.144.1.10:8080'
        # elif request.url.startswith("https://"):
        #     request.meta['proxy']="https://"+'10.144.1.10:8080'
        return None


    def process_response(self, request, response, spider):
        """

        :param request:
        :param response:
        :param spider:
        :return:
        """

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response


    def process_exception(self, request, exception, spider):
        """
        
        :param request:
        :param exception:
        :param spider:
        :return:
        """
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

class AreaSpiderMiddleware(object):
    def process_request(self, request, spider):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe')
        self.driver.get(request.url)
        time.sleep(1)
        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(1)
        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(1)
        html = self.driver.page_source
        self.driver.quit()
        return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
                                        request=request)