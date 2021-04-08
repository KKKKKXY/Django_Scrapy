# import needed lib
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
# import own lib
from .spiders.selenium_getCookie_Thai import *
from .different_run_spider import *

@api_view(['GET', 'POST'])
@csrf_exempt
def getThaiCaptchaEmail(request):
    if request.method == 'POST':
        name = 'Scrapy_Actions'
        configure_logging(install_root_handler=False)
        # clean up .log file
        with open('/backend/log/Scrapy_Actions.log', 'w'):
            pass
        # record logging
        logging.basicConfig(
            filename='log/%s.log' % name,
            format='%(levelname)s %(asctime)s: %(message)s',
            level=logging.DEBUG
        )
        print('Getting Thai email enclose with captcha code')
        logging.warning('Getting Thai email enclose with captcha code')
        # get capctcha and send email including capctcha
        getCaptchaEmail()
        return Response({"message": "send capctha code email done"})
    return Response({"message": "other request method"})

# according to the number of browsers user selected to start scrape
def number_of_browser_to_scrapy(num, selectThai):
    if num == 1:
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
        logging.error('invalid the number of browser')

@api_view(['POST'])
@csrf_exempt
def run_thai_spider(request):
    name = 'Scrapy_Actions'
    if request.method == 'POST':
        # get the passing variables from frontend
        captchaCode = request.data['captchaCode']
        thaiBrowser = request.data['thaiBrowser']
        selectThai  = request.data['selectThai']
        # with open('/backend/log/Scrapy_Actions.log', 'w'):
        #     pass
        configure_logging(install_root_handler=False)
        logging.basicConfig(
            filename='log/%s.log' % name,
            format='%(levelname)s %(asctime)s: %(message)s',
            level=logging.DEBUG
        )
        logging.warning('You selected the number of browser to scrapy is: ' + thaiBrowser)
        logging.warning('You Selected file is: ' + selectThai)
        # number_of_browser_to_scrapy(int(thaiBrowser), selectThai)

        try:
            # verify whether the cookie is valid
            is_error = verifyCaptchaAndLogin(captchaCode)
            if is_error:
                logging.warning('Please get a new capctha code screenshot and input capctha code again!')
            else:
                # store cookie
                storeCookie()
                # start to run crawlers
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
                        # send email
                        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                        response = sg.send(message)
                        print('Scrapy finished message send.')
                        logging.warning('Scrapy finished message send.')
                        logging.info('finish this spider:%s\n\n' % 'run_thai_spider')
                    except Exception as e:
                        # error occurs when sending email
                        print('Send scrapy finished message failed.')
                        print(e)
                        logging.warning('Send scrapy finished message failed.')
                        logging.error(e)

                except Exception as e:
                    # error occurs when run crawlers
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
            # error occurs when run selenium part
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

# to get email format
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
