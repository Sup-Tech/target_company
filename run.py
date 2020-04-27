from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

setting = get_project_settings()
process = CrawlerProcess(setting)

for spider_name in process.spiders.list():
    if spider_name == 'job58' or spider_name == 'job51':
        print("Running spider %s" % (spider_name))
        process.crawl(spider_name)

process.start()
