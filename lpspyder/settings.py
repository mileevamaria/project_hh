# -*- coding: utf-8 -*-

# Scrapy settings for lpspyder project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lpspyder'

SPIDER_MODULES = ['lpspyder.spiders']
NEWSPIDER_MODULE = 'lpspyder.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lpspyder (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
# COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'hhuid=YPz1MucmeOvbhV1J!ApIUQ--; regions=1; _ga=GA1.1.804882805.1565129739; _ym_uid=1565129739284807948; _ym_d=1565129739; __zzat58=MDA0dBA=Fz2+aQ==; _ga=GA1.2.2023020497.1565965474; region_clarified=NOT_SET; collapse_saved_search_vacancy_subscription=true; hhtoken=Cf1lqOdqQjEdLgBMrqanUUMNAw!f; _xsrf=0694145b085b7ac875907a0de867203f; _xsrf=0694145b085b7ac875907a0de867203f; display=desktop; hhrole=anonymous; GMT=3; _gid=GA1.1.2091905903.1568816421; _ym_isad=1; _ym_visorc_156828=w; total_searches=9; gssc58=SX/nRSKHaiGY568bC5W+v6jtedKP4MbuTLyWlFoAHyOoHQd56F1fbCF5DX7kRu12cys1IX0reO89uv3qoc8cqG46DB53syeMniq+R7Vhz0exBCQfkvADuhhhWBaGYad4KiaTmCwOTUQXmFd3DenbKcYjSvFXuRWa11bjkYc=; cfids58=vsKKNnfxgLemuibnaGuqTyOiwzLmSj4kHGqGm5RXzUXEqep4EaehN4g1JdpKxzb8m4HtzmWbBXeHQEIthbuWDwLmDCOI27diVDxfLc7MkPVvUeI33f6itbUP97gHCVKwzAvcw7HPEw5bnVK66v7CEqlLhXcYd5UOlCBgxuc=; gssc58=SX/nRSKHaiGY568bC5W+v6jtedKP4MbuTLyWlFoAHyOoHQd56F1fbCF5DX7kRu12cys1IX0reO89uv3qoc8cqG46DB53syeMniq+R7Vhz0exBCQfkvADuhhhWBaGYad4KiaTmCwOTUQXmFd3DenbKcYjSvFXuRWa11bjkYc=; fgssc58=243f23bab90cf12fb4ec64d10e1343a3c1c0886b; cfids58=vumBZazgVaMtrHLdchzB2GZv88EaC0fN715FyCmRGsCq5IbS8rX6Tp/EH3CS1xx0sjQAC4CZ3qI2FsTXCypdtiKV/9EhapXMQSd55XDB/WfPUW1pUJa52I/bdeG4NyzOZYqlTMNaXAhviGj1aLNMpLgC679itoVhwEhHl8o=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'lpspyder.middlewares.lpspyderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 543,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 546,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 700,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 701,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 548,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'lpspyder.pipelines.lpspyderPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 2
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

REDIRECT_ENABLED = True

RETRY_ENABLED = True
RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 405, 400]
#DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'


MYSQL_CONNECTION = "mysql+pymysql://root:23041995@localhost/project_hh"
