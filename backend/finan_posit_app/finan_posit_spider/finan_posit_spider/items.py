import scrapy

# class FinanPositSpiderItem(scrapy.Item):
#     company_id              = scrapy.Field()
#     accounts_receive        = scrapy.Field()
#     inventory               = scrapy.Field()
#     t_curr_asset            = scrapy.Field()
#     proper_plant_equip      = scrapy.Field()
#     t_nonCurr_asset         = scrapy.Field()
#     t_assets                = scrapy.Field()
#     t_curr_liab             = scrapy.Field()
#     t_nonCurr_liab          = scrapy.Field()
#     t_liab_and_equity       = scrapy.Field()
#     equity                  = scrapy.Field()
#     t_liab_and_equity       = scrapy.Field()

class FinanYearDetailItem(scrapy.Item):
    company_id  = scrapy.Field()
    year        = scrapy.Field()
    amount      = scrapy.Field()
    change      = scrapy.Field()