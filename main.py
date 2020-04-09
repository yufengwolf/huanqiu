import ssl
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils import log
from scrapy.utils.misc import load_object
from twisted.internet import defer
from twisted.internet import reactor

import config


# 忽略证书校验
ssl._create_default_https_context = ssl._create_unverified_context

# 初始化爬虫日志
log.configure_logging()

runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
	for name in ['finance_huanqiu_com']:
		settings = Settings()
		settings.setmodule(name + '.settings')
		yield runner.crawl(Crawler(load_object('%s.spiders.FinanceSpider' % (name.lower(),)), settings))
	reactor.stop()

crawl()

#调整线程池最大线程数
reactor.suggestThreadPoolSize(config.REACTOR_THREADPOOL_MAXSIZE)

reactor.run()

