import scrapy

class RatioYearItem(scrapy.Item):
    company_id      = scrapy.Field()
    year            = scrapy.Field()
    ratio           = scrapy.Field()