from scrapy.utils.project import get_project_settings
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from django.views.decorators.csrf import csrf_exempt
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
# from scrapy.crawler import Crawler
from crochet import setup
from scrapy_thai_app.thai_spider.thai_spider.spiders.dbdcrawler_Thai import DbdcrawlerSpider1, DbdcrawlerSpider2, DbdcrawlerSpider3, DbdcrawlerSpider4, DbdcrawlerSpider5
from django.shortcuts import render, redirect
# from .thai_spider import settings as my_settings

# runner = CrawlerRunner(get_project_settings())
#     runner.crawl(DbdcrawlerSpider1)

#     d = runner.join()
#     d.addBoth(lambda _: reactor.stop())
#     # reactor.callFromThread(notThreadSafe, 3)
#     reactor.run()


@csrf_exempt
def runspider(request):
    # response = Response()
    print(request)
    if request.method == "POST":
        print(request.POST)
        # print('Runspider------------------------------------------------------------------------------->')
        print('Runspider------------------------------------------------------------------------------->')
        name = 'thai_scrapy'
        configure_logging(install_root_handler=False)
        logging.basicConfig(
            filename='log/%s.log' % name,
            format='%(levelname)s %(asctime)s: %(message)s',
            level=logging.DEBUG
        )
        options = {
            'CONCURRENT_ITEMS': 250,
            # 'USER_AGENT': 'Googlebot/2.1 (+http://www.google.com/bot.html)',
            'CONCURRENT_REQUESTS': 30,
            'DOWNLOAD_DELAY': 0.5,
            'COOKIES_ENABLED': False,
        }
        crawler_settings = Settings()
        # settings = get_project_settings()
        setup()
        # crawler_settings.setmodule(my_settings)
        runner = CrawlerRunner(settings=crawler_settings)
        # settings.update(options)
        print('Runspider------------------------------------------------------------------------------->')
        # process = CrawlerProcess(get_project_settings())
        # runner = CrawlerRunner(settings)
        print('Runspider------------------------------------------------------------------------------->')
        try:
            logging.info('runspider start spider:%s' % name)
            # process.crawl(DbdcrawlerSpider1)
            # process.crawl(DbdcrawlerSpider2)
            # process.crawl(DbdcrawlerSpider3)
            # process.crawl(DbdcrawlerSpider4)
            # process.crawl(DbdcrawlerSpider5)

            runner.crawl(DbdcrawlerSpider1)
            print(
                'Runspider------------------------------------------------------------------------------->')
            # runner.crawl(DbdcrawlerSpider2)
            d = runner.join()
            print(
                'Runspider------------------------------------------------------------------------------->')
            d.addBoth(lambda _: reactor.stop())
            print(
                'Runspider------------------------------------------------------------------------------->')
            reactor.run()
            print(
                'Runspider------------------------------------------------------------------------------->')
            # process.start()
        except Exception as e:
            logging.exception('runspider spider:%s exception:%s' % (name, e))
            print(
                'Runspider------------------------------------------------------------------------------->')

        logging.debug('finish this spider:%s\n\n' % name)
        logging.debug('-----------------------------------------------------')
        return redirect("/admin/")
    return redirect("/getData/")


# process = CrawlerProcess(get_project_settings())
# process.crawl(DbdcrawlerSpider1)
# # process.crawl(DbdcrawlerSpider2)
# # process.crawl(DbdcrawlerSpider3)
# # process.crawl(DbdcrawlerSpider4)
# # process.crawl(DbdcrawlerSpider5)
# process.start()
