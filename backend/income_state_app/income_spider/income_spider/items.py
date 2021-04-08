import scrapy

class IncomeYearItem(scrapy.Item):
    company_id  = scrapy.Field()
    year        = scrapy.Field()
    amount      = scrapy.Field()
    change      = scrapy.Field()