import scrapy

class PositYearItem(scrapy.Item):
    company_id      = scrapy.Field()
    year            = scrapy.Field()
    amount          = scrapy.Field()
    change          = scrapy.Field()