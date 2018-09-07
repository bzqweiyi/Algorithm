# -*- coding: utf-8 -*-

# Scrapy settings for corpus_health project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from decouple import config

BOT_NAME = 'corpus_health'

SPIDER_MODULES = ['corpus_health.spiders']
NEWSPIDER_MODULE = 'corpus_health.spiders'


MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'corpus'
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'

MONGODB_URI = config('MONGODB_URI', default='mongodb://localhost:27017')
MONGODB_DB = config('MONGODB_DB', default="article")
MONGODB_COLLECTION = config('MONGODB_COLLECTION', default="info_tnb39net")


LOG_ENABLED = True                  # 默认: True，启用logging
LOG_ENCODING = 'utf-8'              # 默认: 'utf-8'，logging使用的编码
# LOG_FILE = 'logging/corpus_health.log'      # 默认: None，logging输出的文件名
LOG_LEVEL = 'DEBUG'                 # 默认: 'DEBUG'，log的最低级别
LOG_STDOUT = False                  # 默认: False，如果为 True，进程所有的标准输出(及错误)将会被重定向到log中。例如，执行 print 'hello' ，其将会在Scrapy log中显示。
LOG_SHORT_NAMES = False             # 显示到模块名，True只显示root
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'


DOWNLOAD_TIMEOUT = 20

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'corpus_health (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# DEPTH_LIMIT = 4
# DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'corpus_health.middlewares.CorpusHealthSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'corpus_health.middlewares.RotateUserAgentMiddleware': 1,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    # 'corpus_health.middlewares.ProxyMiddleware': 125,
}


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'corpus_health.pipelines.MongoCorpusHealthPipeline': 300,
    # 'corpus_health.pipelines.MongoMedicinePipeline': 300,
    'corpus_health.pipelines.MongoNewsPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

SCHEDULER = "scrapy_redis.scheduler.Scheduler"  #启用Redis调度存储请求队列
SCHEDULER_PERSIST = True    #不清除Redis队列、这样可以暂停/恢复 爬取
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  #确保所有的爬虫通过Redis去重
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
REDIS_HOST = 'localhost'  # 也可以根据情况改成 localhost
REDIS_PORT = 6379

