import scrapy

# class FinanRatioSpiderItem(scrapy.Item):
#     pass

class RatioYearDetailItem(scrapy.Item):
    company_id  = scrapy.Field()
    year        = scrapy.Field()
    ratio      = scrapy.Field()