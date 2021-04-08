from itemadapter import ItemAdapter
import json
import logging
import re
# import own lib
from .reg import *
from scrapy_thai_app.models import *

class ThaiSpiderPipeline(object):
    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # assign item values into each variable
        raw_company_id          = item['company_id']
        company_type            = item['company_type']
        status                  = item['status']
        objective               = item['objective']
        raw_directors           = item['directors']
        raw_company_name        = item['company_name']
        raw_bussiness_type      = item['bussiness_type']
        raw_address             = item['address']
        tel                     = item['tel']
        fax                     = item['fax']
        website                 = item['website']
        email                   = item['email']
        last_registered_id      = item['last_registered_id']
        raw_fiscal_year         = item['fiscal_year']

        #clean data
        directors                   = directors_convert(raw_directors)
        bussiness_type              = business_type_separater(raw_bussiness_type)[1]
        bussiness_type_code         = business_type_separater(raw_bussiness_type)[0]
        company_id                  = re.split(':', raw_company_id)[1].strip()
        company_name                = re.split(':', raw_company_name)[1].strip()
        street                      = address_separater(raw_address)[0]
        subdistrict                 = address_separater(raw_address)[1]
        district                    = address_separater(raw_address)[2]
        province                    = address_separater(raw_address)[3]
        address                     = address_separater(raw_address)[4]
        fiscal_year                 = fiscal_year_convert(raw_fiscal_year)
        if company_id == None or company_id == '':
            company_id = '-'
        if company_name == None or company_name == '':
            company_name = '-'
        if company_type == 'No Data':
            company_type = '-'
        if status == 'No Data':
            status = '-'
        if address == None or address == '':
            address = '-'
        if objective == 'No Data':
            objective = '-'
        if directors == None or directors == '':
            directors = '-'
        if bussiness_type == 'No Data' or bussiness_type == None or bussiness_type == '':
            bussiness_type = '-'
        if bussiness_type_code == 'No Data' or bussiness_type_code == None or bussiness_type_code == '':
            bussiness_type_code = '-'
        if tel == 'No Data':
            tel = '-'
        if fax == 'No Data':
            fax = '-'
        if website == 'No Data':
            website = '-'
        if email == 'No Data':
            email = '-'
        if last_registered_id == 'No Data':
            last_registered_id = '-'
        if fiscal_year == 'No Data' or fiscal_year == '':
            fiscal_year = '-'
        if street == None or street == '':
            street = '-'
        if subdistrict == None or subdistrict == '':
            subdistrict = '-'
        if district == None or district == '':
            district = '-'
        if province == None or province == '':
            province = '-'

        # declare an object, type is  DBDCompany_Thai
        new_item = DBDCompany_Thai()
        # filter whether there is already a company in database
        qs = DBDCompany_Thai.objects.all().filter(company_id=company_id).first()
        if not qs:
            # create a new company and save data into database
            print(' ----> Store ' + company_id + ' a new company information...')
            logging.info(' ----> Store ' + company_id + ' a new company information...')
            new_item.company_name                   = company_name
            new_item.company_id                     = company_id
            new_item.company_type                   = company_type
            new_item.company_status                 = status
            new_item.company_address                = address
            new_item.company_objective              = objective
            new_item.company_directors              = directors
            new_item.company_bussiness_type         = bussiness_type
            new_item.company_bussiness_type_code    = bussiness_type_code
            new_item.company_street                 = street
            new_item.company_subdistrict            = subdistrict
            new_item.company_district               = district
            new_item.company_province               = province
            new_item.company_tel                    = tel
            new_item.company_fax                    = fax
            new_item.company_website                = website
            new_item.company_email                  = email
            new_item.company_last_registered_id     = last_registered_id
            new_item.company_fiscal_year            = fiscal_year
            
            new_item.save()
            print(' ----- Store company: ' + new_item.company_id + ' finished =====')
            logging.info(' ----- Store company: ' + new_item.company_id + ' finished =====')

        else:
            # updata company's information from database
            is_updated = False
            print(' ----> Check and update ' + company_id + ' company information...')
            logging.info(' ----> Check and update ' + company_id + ' company information...')
            if qs.company_name != company_name:
                print(' >>>>>>>>>> Company NAME is changed, updating...')
                logging.warning(' >>>>>>>>>> Company NAME is changed, updating...')
                qs.company_name = company_name
                is_updated = True

            if qs.company_type != company_type:
                print(' >>>>>>>>>> Company TYPE is changed, updating...')
                logging.warning(' >>>>>>>>>> Company TYPE is changed, updating...')
                qs.company_type = company_type
                is_updated = True

            if qs.company_status != status:
                print(' >>>>>>>>>> Company STATUS is changed, updating...')
                logging.warning(' >>>>>>>>>> Company STATUS is changed, updating...')
                qs.company_status = status
                is_updated = True

            if qs.company_address != address:
                print(' >>>>>>>>>> Company ADDRESS is changed, updating...')
                logging.warning(' >>>>>>>>>> Company ADDRESS is changed, updating...')
                qs.company_address = address
                is_updated = True

            if qs.company_objective != objective:
                print(' >>>>>>>>>> Company OBJECTIVE is changed, updating...')
                logging.warning(' >>>>>>>>>> Company OBJECTIVE is changed, updating...')
                qs.company_objective = objective
                is_updated = True

            if qs.company_directors != directors:
                print(' >>>>>>>>>> Company DIRECTORS is changed, updating...')
                logging.warning(' >>>>>>>>>> Company DIRECTORS is changed, updating...')
                qs.company_directors = directors
                is_updated = True

            if qs.company_bussiness_type != bussiness_type:
                print(' >>>>>>>>>> Company BUSSINESS TYPE is changed, updating...')
                logging.warning(' >>>>>>>>>> Company BUSSINESS TYPE is changed, updating...')
                qs.company_bussiness_type = bussiness_type
                is_updated = True

            if qs.company_bussiness_type_code != bussiness_type_code:
                print(' >>>>>>>>>> Company BUSSINESS TYPE CODE is changed, updating...')
                logging.warning(' >>>>>>>>>> Company BUSSINESS TYPE CODE is changed, updating...')
                qs.company_bussiness_type_code = bussiness_type_code
                is_updated = True

            if qs.company_street != street:
                print(' >>>>>>>>>> Company STREET is changed, updating...')
                logging.warning(' >>>>>>>>>> Company STREET is changed, updating...')
                qs.company_street = street
                is_updated = True

            if qs.company_subdistrict != subdistrict:
                print(' >>>>>>>>>> Company SUBDISTRICT is changed, updating...')
                logging.warning(' >>>>>>>>>> Company SUBDISTRICT is changed, updating...')
                qs.company_subdistrict = subdistrict
                is_updated = True

            if qs.company_district != district:
                print(' >>>>>>>>>> Company DISTRICT is changed, updating...')
                logging.warning(' >>>>>>>>>> Company DISTRICT is changed, updating...')
                qs.company_district = district
                is_updated = True

            if qs.company_province != province:
                print(' >>>>>>>>>> Company PROVINCE is changed, updating...')
                logging.warning(' >>>>>>>>>> Company PROVINCE is changed, updating...')
                qs.company_province = province
                is_updated = True

            if qs.company_tel != tel:
                print(' >>>>>>>>>> Company TEL. is changed, updating...')
                logging.warning(' >>>>>>>>>> Company TEL. is changed, updating...')
                qs.company_tel = tel
                is_updated = True

            if qs.company_fax != fax:
                print(' >>>>>>>>>> Company FAX is changed, updating...')
                logging.warning(' >>>>>>>>>> Company FAX is changed, updating...')
                qs.company_fax = fax
                is_updated = True

            if qs.company_website != website:
                print(' >>>>>>>>> Company WEBSITE is changed, updating...')
                logging.warning(' >>>>>>>>>> Company WEBSITE is changed, updating...')
                qs.company_website = website
                is_updated = True

            if qs.company_email != email:
                print(' >>>>>>>>>> Company EMAIL is changed, updating...')
                logging.warning(' >>>>>>>>>> Company EMAIL is changed, updating...')
                qs.company_email = email
                is_updated = True

            if qs.company_last_registered_id != last_registered_id:
                print(' >>>>>>>>>> Company LAST REGISTERED ID is changed, updating...')
                logging.warning(' >>>>>>>>>> Company LAST REGISTERED ID is changed, updating...')
                qs.company_last_registered_id = last_registered_id
                is_updated = True

            if qs.company_fiscal_year != fiscal_year:
                print(' >>>>>>>>>> Company FISCAL YEAR is changed, updating...')
                logging.warning(' >>>>>>>>>> Company FISCAL YEAR is changed, updating...')
                qs.company_fiscal_year = fiscal_year
                is_updated = True

            qs.is_changed = is_updated
            qs.save()
            if is_updated:
                print(' ---------- Update company: ' + qs.company_id + ' informtion finished ==========')
                logging.critical(' ---------- Update company: ' + qs.company_id + ' informtion finished ==========')
            else:
                print(' ---------- The company have not changed information ==========')
                logging.critical(' ---------- The company have not changed information ==========')

        return item