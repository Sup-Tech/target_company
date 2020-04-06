# -*- coding: utf-8 -*-
import scrapy


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['job.51job.com']
    start_urls = ['http://job.51job.com/']

    def parse(self, response):
        pass
