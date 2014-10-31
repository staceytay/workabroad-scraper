# Scrapy settings for workabroad project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'workabroad'

SPIDER_MODULES = ['workabroad.spiders']
NEWSPIDER_MODULE = 'workabroad.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'workabroad (+http://www.yourdomain.com)'

DEPTH_LIMIT = 0 # Default is 0
DOWNLOAD_DELAY = 10
RANDOMIZE_DOWNLOAD_DELAY = True
