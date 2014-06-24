# Scrapy settings for mmonly project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'mmonly'

SPIDER_MODULES = ['mmonly.spiders']
NEWSPIDER_MODULE = 'mmonly.spiders'


ITEM_PIPELINES = ['mmonly.MyImagesPipeline.MyImagesPipeline','mmonly.pipelines.MmonlyPipeline']
#ITEM_PIPELINES = ['mmonly.MyImagesPipeline.MyImagesPipeline']
#ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']

IMAGES_STORE = r'c:\1A_Image_Store_Temp'
persist = r'c:\0_persist'

#RETRY_HTTP_CODES = [500, 502, 504, 503, 400, 408]



COOKIES_ENABLED = False
#LOG_LEVEL = 'INFO'
#LOG_FILE = 'c:\log.txt'
#LOG_STDOUT = True
#CONCURRENT_ITEMS = 10
#CONCURRENT_REQUESTS = 1
#CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 0.25 
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'
'''
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'
'''
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mmonly (+http://www.yourdomain.com)'
