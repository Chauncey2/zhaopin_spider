from scrapy.cmdline import execute
execute(["scrapy","crawl","job_spider"])

'''
爬取职位关键词的代码，运行需要关闭管道文件（待优化）
'''
# execute(["scrapy","crawl","keywords_spider","-o","keywords.json"])



