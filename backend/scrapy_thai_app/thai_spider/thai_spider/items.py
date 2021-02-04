# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ThaiSpiderItem(scrapy.Item):
    company_id              = scrapy.Field()
    company_name            = scrapy.Field()
    company_type            = scrapy.Field()
    status                  = scrapy.Field()
    objective               = scrapy.Field()
    directors               = scrapy.Field()
    bussiness_type          = scrapy.Field()
    address                 = scrapy.Field()
    tel                     = scrapy.Field()
    fax                     = scrapy.Field()
    website                 = scrapy.Field()
    email                   = scrapy.Field()
    last_registered_id      = scrapy.Field()
    fiscal_year             = scrapy.Field()
