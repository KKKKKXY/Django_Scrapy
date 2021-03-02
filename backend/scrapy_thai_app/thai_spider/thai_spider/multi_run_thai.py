from scrapy.utils.project import get_project_settings
import logging
from django.views.decorators.csrf import csrf_exempt
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from .spiders.selenium_getCookie_Thai import *
from .spiders.dbdcrawler_Thai1 import DbdcrawlerSpider1
from .spiders.dbdcrawler_Thai2 import DbdcrawlerSpider2
from .spiders.dbdcrawler_Thai3 import DbdcrawlerSpider3
from .spiders.dbdcrawler_Thai4 import DbdcrawlerSpider4
from .spiders.dbdcrawler_Thai5 import DbdcrawlerSpider5

from string import Template
from sendgrid import SendGridAPIClient
import base64
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.data_reader.excel_reader import *
from backend.data_reader.pdf_reader import *

@api_view(['POST'])
@csrf_exempt
def getThaiCaptchaEmail(request):
    print('getThaiCaptchaEmail')
    if request.method == 'POST':
        name = 'Scrapy_Actions'
        configure_logging(install_root_handler=False)
        with open('/backend/log/Scrapy_Actions.log', 'w'):
            pass
        logging.basicConfig(
            filename='log/%s.log' % name,
            format='%(levelname)s %(asctime)s: %(message)s',
            level=logging.DEBUG
        )
        getCaptchaEmail()
        return Response({"message": "send capctha code email done"})
    return Response({"message": "other request method"})

def number_of_browser_to_scrapy(num, selectThai):
    print('selectThai is: ' + selectThai)
    runner = CrawlerRunner(get_project_settings())
    if num == 1:
        runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
    elif num == 2:
        runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
        runner.crawl(DbdcrawlerSpider2, cid=random_company(selectThai))
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
    elif num == 3:
        runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
        runner.crawl(DbdcrawlerSpider2, cid=random_company(selectThai))
        runner.crawl(DbdcrawlerSpider3, cid=random_company(selectThai))
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
    elif num == 4:
        runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
        runner.crawl(DbdcrawlerSpider2, cid=random_company(selectThai))
        runner.crawl(DbdcrawlerSpider3, cid=random_company(selectThai))
        runner.crawl(DbdcrawlerSpider4, cid=random_company(selectThai))
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
    elif num == 5:
        runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
        runner.crawl(DbdcrawlerSpider2, cid=random_company(selectThai))
        runner.crawl(DbdcrawlerSpider3, cid=random_company(selectThai))
        runner.crawl(DbdcrawlerSpider4, cid=random_company(selectThai))
        runner.crawl(DbdcrawlerSpider5, cid=random_company(selectThai))
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
    else:
        return 'invalid the number of browser'

def random_company(file_name):
    file_type = file_name.rpartition('.')[-1]
    print('file_type is: '+ file_type)
    # excel_path
    if file_type == 'xlsx' or file_type == 'csv':
        excel_path = '/backend/media/xlsx/'+file_name
        print(excel_path)
        companies_id = get_cid_from_excel(excel_path)
    # pdf_path
    elif file_type == 'pdf':
        pdf_path = '/backend/media/pdf/'+file_name
        print(pdf_path)
        pdf_to_excel_path = '/backend/media/pdf_convert_excel/dbd_from_pdf_thai.xlsx'
        # convert_pdf_to_excel(pdf_path, pdf_to_excel_path)
        pdf_to_excel_path = '/backend/scrapy_thai_app/thai_spider/thai_spider/spiders/db/dbd_from_pdf_thai.xlsx'
        companies_id = get_cid_from_pdf(pdf_to_excel_path)
    else:
        print('Invaid')
    return companies_id

@api_view(['POST'])
@csrf_exempt
def run_thai_spider(request):
    name = 'Scrapy_Actions'
    print('run_thai_spider')
    if request.method == 'POST':
        captchaCode = request.data['captchaCode']
        thaiBrowser = request.data['thaiBrowser']
        selectThai = request.data['selectThai']

        configure_logging(install_root_handler=False)
        logging.basicConfig(
            filename='log/%s.log' % name,
            format='%(levelname)s %(asctime)s: %(message)s',
            level=logging.DEBUG
        )
        logging.warning('You selected the number of browser to scrapy is: ' + thaiBrowser)
        logging.warning('You Selected file is: ' + selectThai)

        try:
            # get and store cookie
            is_error = verifyCaptchaAndLogin(captchaCode)
            if is_error:
                logging.warning('Please get a new capctha code screenshot and input capctha code again!')
            else:
                storeCookie()
                # start to run spiders
                # runner = CrawlerRunner(get_project_settings())
                try:
                    logging.info('runspider start spider:%s' % name)
                    number_of_browser_to_scrapy(int(thaiBrowser), selectThai)
                    # runner.crawl(DbdcrawlerSpider1)
                    # runner.crawl(DbdcrawlerSpider2)
                    # runner.crawl(DbdcrawlerSpider3)
                    # runner.crawl(DbdcrawlerSpider4)
                    # runner.crawl(DbdcrawlerSpider5)
                    # d = runner.join()
                    # d.addBoth(lambda _: reactor.stop())
                    # reactor.run()

                    # send finish email to user
                    message_template = read_template('/backend/email_msg/finish_scrapy.txt')
                    attachment_file_name = 'Scrapy_Actions.log'
                    message = Mail(
                        from_email='myaploy@gmail.com',
                        to_emails='xingyuan_kang@elearning.cmu.ac.th',
                        subject='Inform: Scrapy Finished!',
                        html_content=message_template.substitute(ATTACHMENTFILENAME=attachment_file_name)
                    )
                    # add .log attachment
                    file_path = '/backend/log/Scrapy_Actions.log'
                    with open(file_path, 'rb') as f:
                        data = f.read()
                        f.close()
                    encoded = base64.b64encode(data).decode()
                    attachment = Attachment()
                    attachment.file_content = FileContent(encoded)
                    attachment.file_type = FileType('application/log')
                    attachment.file_name = FileName('Scrapy_Actions.log')
                    attachment.disposition = Disposition('attachment')
                    message.attachment = attachment
                    try:
                        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                        response = sg.send(message)
                        print('Message Send.')
                        logging.warning('Message Send.')
                        logging.info('finish this spider:%s\n\n' % name)
                    except Exception as e:
                        print(e)
                        logging.error(e)

                except Exception as e:
                    logging.exception('runspider spider:%s exception:%s' % (name, e))
                    message_template = read_template('/backend/email_msg/reactor_restartable_error.txt')
                    attachment_file_name = 'Scrapy_Actions.log'
                    message = Mail(
                        from_email='myaploy@gmail.com',
                        to_emails='xingyuan_kang@elearning.cmu.ac.th',
                        subject='Warning: Scrapy error happend!',
                        html_content=message_template.substitute(ERROR=e)
                    )
                    # add .log attachment
                    file_path = '/backend/log/Scrapy_Actions.log'
                    with open(file_path, 'rb') as f:
                        data = f.read()
                        f.close()
                    encoded = base64.b64encode(data).decode()
                    attachment = Attachment()
                    attachment.file_content = FileContent(encoded)
                    attachment.file_type = FileType('application/log')
                    attachment.file_name = FileName('Scrapy_Actions.log')
                    attachment.disposition = Disposition('attachment')
                    message.attachment = attachment
                    try:
                        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                        response = sg.send(message)
                        print('Message Send.')
                        logging.warning('Message Send.')
                    except Exception as e:
                        print(e)
                        logging.error(e)
                logging.info('------------------------------------------')
    
        except Exception as e:
            logging.exception('Get and store cookie:%s exception:%s' % (name, e))
            message_template = read_template('/backend/email_msg/error.txt')
            message = Mail(
                from_email='myaploy@gmail.com',
                to_emails='xingyuan_kang@elearning.cmu.ac.th',
                subject='Warning: Error happend!',
                html_content=message_template.substitute(ERROR=e)
            )
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print('Message Send.')
                logging.warning('Message Send.')
            except Exception as e:
                print(e)
                logging.error(e)
        return Response({"message": "Scrapy Thai Done!"})
    return Response({"message": "Got some data!", "data": request.data})


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
