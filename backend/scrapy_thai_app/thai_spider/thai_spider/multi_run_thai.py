import logging
import base64
from django.views.decorators.csrf import csrf_exempt
from scrapy.utils.log import configure_logging
from string import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .spiders.selenium_getCookie_Thai import *
from .different_run_spider import *

@api_view(['GET'])
@csrf_exempt
def getThaiCaptchaEmail(request):
    print('getThaiCaptchaEmail')
    if request.method == 'GET':
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
    # runner = CrawlerRunner(get_project_settings())
    if num == 1:
        # d = runner.join()
        # d.addBoth(lambda _: reactor.stop())
        # reactor.run()
        run_1(selectThai)
    elif num == 2:
        run_2(selectThai)
    elif num == 3:
        run_3(selectThai)
    elif num == 4:
        run_4(selectThai)
    elif num == 5:
        run_5(selectThai)
    else:
        print('invalid the number of browser')

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
                    logging.info('runspider start spider: run_thai_spider')
                    number_of_browser_to_scrapy(int(thaiBrowser), selectThai)

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
                        print('Scrapy finished message send.')
                        logging.warning('Scrapy finished message send.')
                        logging.info('finish this spider:%s\n\n' % 'run_thai_spider')
                    except Exception as e:
                        print('Send scrapy finished message failed.')
                        print(e)
                        logging.warning('Send scrapy finished message failed.')
                        logging.error(e)
                    # runner.crawl(DbdcrawlerSpider1)
                    # runner.crawl(DbdcrawlerSpider2)
                    # runner.crawl(DbdcrawlerSpider3)
                    # runner.crawl(DbdcrawlerSpider4)
                    # runner.crawl(DbdcrawlerSpider5)
                    # d = runner.join()
                    # d.addBoth(lambda _: reactor.stop())
                    # reactor.run()
                    # if finish == True:
                    # send finish email to user

                except Exception as e:
                    logging.exception('runspider spider:%s exception:%s' % ('run_thai_spider', e))
                    message_template = read_template('/backend/email_msg/scrapy_error.txt')
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
                        print('Scrapy error happend message send.')
                        logging.warning('Scrapy error happend message send.')
                    except Exception as e:
                        print('Send scrapy error happend message failed.')
                        print(e)
                        logging.warning('Send scrapy error happend message failed.')
                        logging.error(e)
                logging.info('------------------------------------------')
    
        except Exception as e:
            logging.exception('Get and store cookie:%s exception:%s' % ('run_thai_spider', e))
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
                print('Error happend message send.')
                logging.warning('Error happend message send.')
            except Exception as e:
                print('Send Error happend message failed.')
                print(e)
                logging.warning('Send Error happend message failed.')
                logging.error(e)
        return Response({"message": "Scrapy Thai Done!"})
    return Response({"message": "Got some data!", "data": request.data})

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
