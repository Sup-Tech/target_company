# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time


class A58Spider(scrapy.Spider):
    name = '58'
    allowed_domains = ['58.com']
    city = input('请输入城市名: ')
    keyword = input('请输入要搜索的职位名称: ')
    first_url = ''

    def start_requests(self):
        browser = webdriver.Chrome()
        print('浏览器启动')
        # 打开58 切换城市的页面
        print('打开58 切换城市的页面')
        browser.get('https://58.com/changecity.html?fullpath=0')
        # 匹配输入的城市的58首页链接
        print('匹配输入的城市的58首页链接')
        tmp = browser.find_elements_by_xpath('//a[@class="content-city"]')
        for i in tmp:
            if i.text == self.city:
                # 打开该城市的58首页链接
                print('打开该城市的58首页链接')
                browser.get(i.get_property('href'))
                # 点击全职招聘
                print('点击全职招聘')
                browser.find_element_by_xpath('//*[@id="zpNav"]/em/a[1]').click()
                # 句柄转到招聘搜索页面
                browser.switch_to.window(browser.window_handles[1])
                # 进行搜索
                browser.find_element_by_xpath('//*[@id="keyword1"]').send_keys(self.keyword)
                browser.find_element_by_xpath('//*[@id="searJob"]').click()
                break
        time.sleep(5)

