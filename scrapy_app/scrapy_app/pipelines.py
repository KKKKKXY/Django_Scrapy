# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy_app.reg import *
import json
from main.models import ScrapyItem

class ScrapyAppPipeline(object):
    def __init__(self, *args, **kwargs):
        self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
        )

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # self.items.append(item)
        print('========================process item====================================')
        print(item)

        raw_company_id          = item['company_id']
        company_type            = item['company_type']
        status                  = item['status']
        objective               = item['objective']
        raw_directors           = item['directors']
        raw_company_name        = item['company_name']
        raw_bussiness_type      = item['bussiness_type']
        raw_address             = item['address']#new
        tel                     = item['tel']
        fax                     = item['fax']
        website                 = item['website']
        email                   = item['email']

        #clean data
        directors           = directors_convert(raw_directors)
        # print(directors_text)
        bussiness_type      = business_type_separater(raw_bussiness_type)[1]
        # print(bussiness_type)
        bussiness_type_code = business_type_separater(raw_bussiness_type)[0]
        # print(bussiness_type_code)
        company_id          = re.split(':', raw_company_id)[1].strip()
        company_name        = re.split(':', raw_company_name)[1].strip()
        # print(company_name)
        street             = address_separater(raw_address)[0]
        subdistrict        = address_separater(raw_address)[1]
        district           = address_separater(raw_address)[2]
        province           = address_separater(raw_address)[3]
        address            = address_separater(raw_address)[4]

        if objective == None or objective == '':
            objective = '-'

        if bussiness_type_code == None or bussiness_type_code == '':
            bussiness_type_code = '-'

        if subdistrict == None or subdistrict == '':
            subdistrict = '-'

        if district == None or district == '':
            district = '-'

        if province == None or province == '':
            province = '-'
            

        self.items.append({
            'company_name': company_name,
            'company_id': company_id,
            'company_type': company_type, 
            'status': status,
            'address': address,
            'objective': objective,
            'directors': directors,
            'bussiness_type': bussiness_type,
            'bussiness_type_code': bussiness_type_code,
            'street': street,
            'subdistrict': subdistrict,
            'district': district,
            'province': province,
            'tel': tel,
            'fax': fax,
            'website': website,
            'email': email,
        })

        new_item = ScrapyItem()

        new_item.company_name           = company_name
        new_item.company_id             = company_id
        new_item.company_type           = company_type
        new_item.status                 = status
        new_item.address                = address
        new_item.objective              = objective
        new_item.directors              = directors
        new_item.bussiness_type         = bussiness_type
        new_item.bussiness_type_code    = bussiness_type_code
        new_item.street                 = street
        new_item.subdistrict            = subdistrict
        new_item.district               = district
        new_item.province               = province
        new_item.tel                    = tel
        new_item.fax                    = fax
        new_item.website                = website
        new_item.email                  = email
        new_item.save()

        print('========================clean data========================')
        print(self.items)
        return item