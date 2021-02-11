from scrapy.utils.project import get_project_settings
import logging
from scrapy.crawler import CrawlerProcess
from django.views.decorators.csrf import csrf_exempt
from scrapy.utils.log import configure_logging

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
# from scrapy.crawler import Crawler

from scrapy_thai_app.thai_spider.thai_spider.spiders.dbdcrawler_Thai import DbdcrawlerSpider1, DbdcrawlerSpider2, DbdcrawlerSpider3, DbdcrawlerSpider4, DbdcrawlerSpider5
from django.shortcuts import render, redirect

@csrf_exempt
def checkout_address_reuse_view(request):
    if request.user.is_authenticated():
        context = {}
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method == "POST":
            print(request.POST)
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + "_address_id"] = shipping_address
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
    return redirect("cart:checkout")


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
            #'USER_AGENT': 'Googlebot/2.1 (+http://www.google.com/bot.html)',
            'CONCURRENT_REQUESTS': 30,
            'DOWNLOAD_DELAY': 0.5,
            'COOKIES_ENABLED': False,
        }
        settings = get_project_settings()
        # settings.update(options)
        print('Runspider------------------------------------------------------------------------------->')
        # process = CrawlerProcess(get_project_settings())
        runner = CrawlerRunner(settings)
        print('Runspider------------------------------------------------------------------------------->')
        try:
            logging.info('runspider start spider:%s' % name)
            # process.crawl(DbdcrawlerSpider1)
            # process.crawl(DbdcrawlerSpider2)
            # process.crawl(DbdcrawlerSpider3)
            # process.crawl(DbdcrawlerSpider4)
            # process.crawl(DbdcrawlerSpider5)

            runner.crawl(DbdcrawlerSpider1)
            print('Runspider------------------------------------------------------------------------------->')
            # runner.crawl(DbdcrawlerSpider2)
            d = runner.join()
            print('Runspider------------------------------------------------------------------------------->')
            d.addBoth(lambda _: reactor.stop())
            print('Runspider------------------------------------------------------------------------------->')
            reactor.run()
            print('Runspider------------------------------------------------------------------------------->')
            # process.start()
        except Exception as e:
            logging.exception('runspider spider:%s exception:%s' % (name, e))
            print('Runspider------------------------------------------------------------------------------->')

        logging.debug('finish this spider:%s\n\n' % name) 
        return redirect("/admin/")
    return redirect("/getData/")


# process = CrawlerProcess(get_project_settings())
# process.crawl(DbdcrawlerSpider1)
# # process.crawl(DbdcrawlerSpider2)
# # process.crawl(DbdcrawlerSpider3)
# # process.crawl(DbdcrawlerSpider4)
# # process.crawl(DbdcrawlerSpider5)
# process.start()

