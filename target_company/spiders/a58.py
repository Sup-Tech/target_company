# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
class A58Spider(scrapy.Spider):
    name = '58'
    allowed_domains = ['58.com']

    def start_requests(self):
        browser = webdriver.Chrome()
        print('浏览器启动')
        browser.get('https://58.com/changecity.html?fullpath=0')
        time.sleep(5)
        browser.quit()
