# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TargetCompanyItem(scrapy.Item):
    # url指纹
    url_fingerprint = scrapy.Field()
    # 公司业务描述
    c_name = scrapy.Field()
    c_scale = scrapy.Field()
    c_desc = scrapy.Field()
    c_addr = scrapy.Field()
    c_industry = scrapy.Field()
    # 职位描述
    job_name = scrapy.Field()
    job_desc = scrapy.Field()
    # 职位页面链接
    job_url = scrapy.Field()
    # 职位权重
    weight = scrapy.Field()
