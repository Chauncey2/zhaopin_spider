# from scrapy.cmdline import execute
# execute(["scrapy","crawl","job_spider"])
# execute(["scrapy","crawl","keywords_spider","-o",'keywords_spider.json'])
# execute(["scrapy","crawl","qiancheng_spider"])

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process=CrawlerProcess(get_project_settings())
# process.crawl('job_spider')
process.crawl('qiancheng_spider')

process.start()

