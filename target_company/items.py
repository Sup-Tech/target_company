# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TargetCompanyItem(scrapy.Item):
    # url指纹
    url_fingerprint = scrapy.Field()
    company_name = scrapy.Field()
    company_location = scrapy.Field()
    # 公司业务描述
    company_desc = scrapy.Field()
    company_scale = scrapy.Field()
    job_name = scrapy.Field()
    # 职位描述
    job_desc = scrapy.Field()

