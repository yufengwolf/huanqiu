# -*- coding: utf-8 -*-

# Scrapy settings for www_ceh_com_cn project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from datetime import datetime

BOT_NAME = 'www_ceh_com_cn'

SPIDER_MODULES = ['www_ceh_com_cn.spiders']
NEWSPIDER_MODULE = 'www_ceh_com_cn.spiders'

COOKIES_ENABLED = True

CONCURRENT_ITEMS = 1024

CONCURRENT_REQUESTS = 64

CONCURRENT_REQUESTS_PER_DOMAIN = 64

DEFAULT_REQUEST_HEADERS = { 'Referer': 'http://www.ceh.com.cn/index.shtml' }

DEPTH_PRIORITY = 1
#add delay
DOWNLOAD_DELAY = 3

#DOWNLOADER_MIDDLEWARES = { 'www_ceh_com_cn.middlewares.DownloaderMiddleware': 543 }

ITEM_PIPELINES = { 'sina.pipelines.SQLSaveRequestPipeline': 300,
                  'www_ceh_com_cn.pipelines.ArticlePipeline': 310,
                  'sina.pipelines.SQLSaveArticlePipeline': 320 }

LOG_ENABLED = True

LOG_ENCODING = 'utf-8'

LOG_FILE = datetime.now().strftime("%Y-%m-%d")+'spider.log'

LOG_LEVEL = 'INFO'

LOG_SHORT_NAMES = False

LOG_STDOUT = False

LOGSTATS_INTERVAL = 60

NEWSPIDER_MODULE = 'www_ceh_com_cn.spiders'

REACTOR_THREADPOOL_MAXSIZE = 256

RETRY_TIMES = 9

ROBOTSTXT_OBEY = False

SPIDER_MIDDLEWARES = { 'www_ceh_com_cn.middlewares.SpiderMiddleware': 543 }

SPIDER_MODULES = ['www_ceh_com_cn.spiders']

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'


