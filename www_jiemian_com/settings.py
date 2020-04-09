# -*- coding: utf-8 -*-
from datetime import datetime


BOT_NAME = 'www_jiemian_com'

COOKIES_ENABLED = True

CONCURRENT_ITEMS = 1024

CONCURRENT_REQUESTS = 64

CONCURRENT_REQUESTS_PER_DOMAIN = 64

DEFAULT_REQUEST_HEADERS = { 'Referer': 'https://www.jiemian.com/' }

DEPTH_PRIORITY = 1
#add delay
DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = { 'www_jiemian_com.middlewares.DownloaderMiddleware': 543 }

ITEM_PIPELINES = { 'sina.pipelines.SQLSaveRequestPipeline': 300,
                  'www_jiemian_com.pipelines.ArticlePipeline': 310,
                  'sina.pipelines.SQLSaveArticlePipeline': 320 }

LOG_ENABLED = True

LOG_ENCODING = 'utf-8'

LOG_FILE = datetime.now().strftime("%Y-%m-%d")+'spider.log'

LOG_LEVEL = 'DEBUG'

LOG_SHORT_NAMES = False

LOG_STDOUT = False

LOGSTATS_INTERVAL = 60

NEWSPIDER_MODULE = 'www_jiemian_com.spiders'

REACTOR_THREADPOOL_MAXSIZE = 256

RETRY_TIMES = 9

ROBOTSTXT_OBEY = False

SPIDER_MIDDLEWARES = { 'www_jiemian_com.middlewares.SpiderMiddleware': 543 }

SPIDER_MODULES = ['www_jiemian_com.spiders']

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
