# -*- coding: utf-8 -*-
import scrapy


class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin'
    allowed_domains = ['zhaopin.com']
    def __init__(self):
        super(ZhaopinSpider, self).__init__()
        city = input('请输入城市: ')
        keyword = input('请输入职位关键词: ')
        city_code = {'杭州':'653', '金华':'659'}
        self.url = 'https://sou.zhaopin.com/?jl={}&kw={}&kt=3'.format(city_code[city],keyword)

    def parse(self, response):
        pass
