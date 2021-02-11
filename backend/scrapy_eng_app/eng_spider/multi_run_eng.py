from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from eng_spider.spiders.dbdcrawler_Eng import DbdcrawlerSpider1, DbdcrawlerSpider2, DbdcrawlerSpider3, DbdcrawlerSpider4, DbdcrawlerSpider5

process = CrawlerProcess(get_project_settings())
process.crawl(DbdcrawlerSpider1)
process.crawl(DbdcrawlerSpider2)
process.crawl(DbdcrawlerSpider3)
process.crawl(DbdcrawlerSpider4)
process.crawl(DbdcrawlerSpider5)
process.start()