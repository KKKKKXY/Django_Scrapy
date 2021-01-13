# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter


# class ScrapyAppPipeline:
#     def process_item(self, item, spider):
#         return item
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
        # And here we are saving our crawled data with django models.
        item = ScrapyItem()
        # print('item--------------------------------------------------')
        # print(item)
        print('items+++++++++++++++++++++++++++++++++++++++++++++++++')
        print(self.items)
        print('self.items[company_id]+++++++++++++++++++++++++++++++++++++++++++++++++')
        print(self.items[0]['company_id'])

        item.company_name = json.dumps(self.items[0]['company_name'], ensure_ascii=False)
        item.company_id = json.dumps(self.items[0]['company_id'], ensure_ascii=False)
        item.company_type = json.dumps(self.items[0]['company_type'], ensure_ascii=False)
        item.status = json.dumps(self.items[0]['status'], ensure_ascii=False)
        item.address = json.dumps(self.items[0]['address'], ensure_ascii=False)
        item.objective = json.dumps(self.items[0]['objective'], ensure_ascii=False)
        item.directors = json.dumps(self.items[0]['directors'], ensure_ascii=False)
        item.bussiness_type = json.dumps(self.items[0]['bussiness_type'], ensure_ascii=False)
        item.bussiness_type_code = json.dumps(self.items[0]['bussiness_type_code'], ensure_ascii=False)
        item.street = json.dumps(self.items[0]['street'], ensure_ascii=False)
        item.subdistrict = json.dumps(self.items[0]['subdistrict'], ensure_ascii=False)
        item.district = json.dumps(self.items[0]['district'], ensure_ascii=False)
        item.province = json.dumps(self.items[0]['province'], ensure_ascii=False)
        item.tel = json.dumps(self.items[0]['tel'], ensure_ascii=False)
        item.fax = json.dumps(self.items[0]['fax'], ensure_ascii=False)
        item.website = json.dumps(self.items[0]['website'], ensure_ascii=False)
        item.email = json.dumps(self.items[0]['email'], ensure_ascii=False)
        item.save()
        print('========================new item====================================')
        print(item.street)


    def process_item(self, item, spider):
        # self.items.append(item)
        print('========================process item====================================')
        print(item)

        company_id              = item['company_id']
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
        directors      = directors_convert(raw_directors)
        # print(directors_text)
        bussiness_type      = business_type_separater(raw_bussiness_type)[1]
        # print(bussiness_type)
        bussiness_type_code = business_type_separater(raw_bussiness_type)[0]
        # print(bussiness_type_code)
        company_name        = re.split(':', raw_company_name)[1].strip()
        # print(company_name)
        street             = address_separater(raw_address)[0]
        subdistrict        = address_separater(raw_address)[1]
        district           = address_separater(raw_address)[2]
        province           = address_separater(raw_address)[3]
        address            = address_separater(raw_address)[4]



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
        print('========================clean data========================')
        print(self.items)
    
        return item