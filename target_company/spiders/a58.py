# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
from ..items import TargetCompanyItem
import hashlib
import sqlite3
from functools import reduce
import json


class A58Spider(scrapy.Spider):
    name = '58'
    allowed_domains = ['58.com']
    city = input('请输入城市名: ')
    keyword = input('请输入要搜索的职位名称: ')
    first_url = ''
    # 一些标志符
    is_final = False
    # 一些计数器
    total = 0
    fingerprint_repeat_error = 0
    company_repeat_error = 0

    def __init__(self):
        super(A58Spider, self).__init__()
        self.conn = sqlite3.connect('target_company.db')
        print('连接数据库')
        self.c = self.conn.cursor()

    def start_requests(self):
        # 设置无头模式
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        print('浏览器启动')
        # 打开58 切换城市的页面
        print('打开 58切换城市的页面')
        browser.get('https://58.com/changecity.html?fullpath=0')
        # 匹配输入的城市的58首页链接
        print('正在匹配 输入的城市的58首页...')
        tmp = browser.find_elements_by_xpath('//a[@class="content-city"]')
        for i in tmp:
            if i.text == self.city or self.city in i.text:
                # 打开该城市的58首页链接
                print('打开该城市的58首页链接')
                browser.get(i.get_property('href'))
                # 点击全职招聘
                print('点击全职招聘')
                browser.find_element_by_xpath('//*[@id="zpNav"]/em/a[1]').click()
                # 句柄转到招聘搜索页面
                print('句柄转到新页面')
                browser.switch_to.window(browser.window_handles[1])
                # 进行搜索
                print('进行搜索')
                browser.find_element_by_xpath('//*[@id="keyword1"]').send_keys(self.keyword)
                browser.find_element_by_xpath('//*[@id="searJob"]').click()
                time.sleep(0.5)
                i = 0
                # 返回 搜索结果页中的所有职位的详情页链接
                while not self.is_final:
                    print('第{}页'.format(i+1))
                    i += 1
                    job_list = browser.find_elements_by_xpath('//div[@class="job_name clearfix"]//a')
                    for job in job_list:
                        url = job.get_attribute('href')
                        finger = url.split('.shtml?')[0]
                        self.fingerprint = hashlib.md5(finger.encode(encoding='utf-8')).hexdigest()
                        # 增量爬虫 指纹去重
                        sql = 'insert into fingerprint values("{}");'.format(self.fingerprint)
                        try:
                            self.c.execute(sql)
                            self.conn.commit()
                        except sqlite3.IntegrityError:
                            self.fingerprint_repeat_error += 1
                        except Exception as e:
                            print(e)
                        else:
                            yield scrapy.Request(url=url, callback=self.parse)
                    try:
                        next = browser.find_element_by_xpath('//a[@class="next"]')
                    except Exception as e:
                        self.is_final = True
                    else:
                        next.click()

                print('一级爬虫结束')

    def parse(self, response):
        """抓取公司信息，职位信息"""
        try:
            company_desc = reduce(lambda x, y: x+y, response.xpath('//div[@class="shiji"]/p/text()').extract())
            company_name = response.xpath('//div[@class="baseInfo_link"]/a/text()').get()
            company_address = response.xpath('//div[@class="pos-area"]/span[2]/text()').get()
            company_scale = response.xpath('//p[@class="comp_baseInfo_scale"]/text()').get().split('-')[0]
            job_name = response.xpath('//span[@class="pos_title"]/text()').get()
            job_desc = reduce(lambda x, y: x+y, response.xpath('//div[@class="des"]/text()').extract())
        except Exception as e:
            print(e)
            print(self.fingerprint)
            sql = "delete from fingerprint where url_md5='{}';".format(self.fingerprint)
            self.c.execute(sql)
            self.conn.commit()
            time.sleep(8)
        # 创建表单变量
        area_id = ''
        company_id = ''
        job_id = ''
        # 插入数据到区域表 并获取该区域的id
        sql = "insert into areas(area) values('{}');".format(self.city)
        try:
            self.c.execute(sql)
        except sqlite3.IntegrityError:
            pass
        except Exception as e:
            print(type(e))
            sql = "select id from areas where area = '{}';".format(self.city)
            area_id = self.c.execute(sql).fetchone()[0]
        else:
            sql = "select max(id) from areas;"
            area_id = self.c.execute(sql).fetchone()[0]
        self.conn.commit()
        # 插入数据到公司信息表 并获取该条目的id
        sql = "insert into companies(company_name, company_address, company_scale, company_desc)" \
              "values('{}', '{}', '{}', '{}');".format(company_name, company_address, company_scale, company_desc)
        try:
            self.c.execute(sql)
        except sqlite3.IntegrityError:
            self.company_repeat_error += 1
        except Exception as e:
            print(e)
            sql = "select id from companies where company_name = '{}';".format(company_name)
            company_id = self.c.execute(sql).fetchone()[0]
        else:
            sql = "select max(id) from companies;"
            company_id = self.c.execute(sql).fetchone()[0]
        # 插入数据到职位数据表 并获取该条目的id
        sql = "insert into jobs(job_name, job_desc) " \
              "values('{}', '{}');".format(job_name, job_desc)
        try:
            self.c.execute(sql)
        except sqlite3.IntegrityError:
            pass
        except Exception as e:
            print(e)
        else:
            sql = "select max(id) from jobs;"
            job_id = self.c.execute(sql).fetchone()[0]
        # 插入爬取数据表数据
        sql = "insert into raw_datas(area_id, company_id, job_id) " \
              "values('{}', '{}', '{}');".format(area_id, company_id, job_id)
        self.c.execute(sql)
        self.conn.commit()

        return

    def close(self, spider, reason):
        print('公司重复次数')
        print(self.company_repeat_error)
        print('指纹重复次数')
        print(self.fingerprint_repeat_error)



