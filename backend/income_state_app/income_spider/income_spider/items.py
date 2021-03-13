import scrapy

# class IncomeSpiderItem(scrapy.Item):
#     company_id                      = scrapy.Field()
#     reve_from_sale_serv             = scrapy.Field()
#     t_reve                          = scrapy.Field()
#     cost_of_goods_sold              = scrapy.Field()
#     gross_profit                    = scrapy.Field()
#     sell_admin_expe                 = scrapy.Field()
#     t_expe                          = scrapy.Field()
#     intere_expe                     = scrapy.Field()
#     profit_before_income_tax        = scrapy.Field()
#     income_tax_expe                 = scrapy.Field()
#     net_profit                      = scrapy.Field()

class IncomeYearDetailItem(scrapy.Item):
    company_id  = scrapy.Field()
    year        = scrapy.Field()
    amount      = scrapy.Field()
    change      = scrapy.Field()