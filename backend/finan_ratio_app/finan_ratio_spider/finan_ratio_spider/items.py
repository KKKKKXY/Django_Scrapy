import scrapy

# class FinanRatioSpiderItem(scrapy.Item):
#     pass

class RatioYearItem(scrapy.Item):
    company_id  = scrapy.Field()
    year        = scrapy.Field()
    ratio      = scrapy.Field()