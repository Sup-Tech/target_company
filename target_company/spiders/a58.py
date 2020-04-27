# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
from ..items import TargetCompanyItem
import hashlib
import sqlite3
from functools import reduce
import json
from threading import Lock


class A58Spider(scrapy.Spider):
    name = 'job58'
    allowed_domains = ['58.com']

    def __init__(self):
        super(A58Spider, self).__init__()
        # 权重
        # company_desc_without_words = input('公司业务介绍里不能有的字词(以空格分隔开)：').split(' ')
        # company_desc_with_words = input('公司业务介绍里能有的字词(以空格分隔开)：').split(' ')
        # job_desc_without_words = input('职位介绍里不能有的字词(以空格分隔开)：').split(' ')
        # job_desc_with_words = input('职位介绍里能有的字词(以空格分隔开)：').split(' ')
        self.c_name_without_words = '厂 工贸 制品 用品 制造'.split(' ')
        self.c_name_with_words = '进出口 科技'.split(' ')
        self.c_desc_without_words = '淘宝 专业生产 生产 工厂 专门生产 主要生产'.split(' ')
        self.c_desc_with_words = '外贸 出口 跨境 电商 贸易 中小额 批发 零售 进出口'.split(' ')
        self.job_desc_without_words = '台账'.split(' ')
        self.job_desc_with_words = ' excel 数据 售前 编写商品 产品编码 表格 新品 编码 erp ERP Excel'.split(' ')
        # 一些标志符
        self.is_final = False
        # 一些计数器
        self.total = 0
        self.fingerprint_repeat_error = 0
        self.company_repeat_error = 0
        self.new_company_num = 0
        self.new_job_num = 0
        # 线程锁
        self.glock = Lock()
        # 连接数据库
        self.conn = sqlite3.connect('target_company.db')
        self.city = input('请输入城市名: ')
        self.keyword = input('请输入要搜索的职位名称: ')
        self.c = self.conn.cursor()
        self.set_area_id()

    def start_requests(self):
        # 处理关键词列表中无效元素
        while '' in self.c_desc_without_words:
            self.c_desc_without_words.remove('')
        while '' in self.c_desc_with_words:
            self.c_desc_with_words.remove('')
        while '' in self.job_desc_without_words:
            self.job_desc_without_words.remove('')
        while '' in self.job_desc_with_words:
            self.job_desc_with_words.remove('')
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
            print('---------\n', company_name, company_scale, company_address, '\n', company_desc, '\n', job_name, '\n', job_desc, '\n---------', sep='')
        except Exception as e:
            print(e)
            print(self.fingerprint)
            sql = "delete from fingerprint where url_md5='{}';".format(self.fingerprint)
            self.c.execute(sql)
            self.conn.commit()
            time.sleep(8)
        if True in [word in company_name for word in self.c_name_without_words]:
            return
        # 创建表单变量
        company_id = ''
        job_id = ''
        # 插入数据到公司信息表 并获取该条目的id
        sql = "insert into companies(company_name, company_address, company_scale, company_desc)" \
              "values('{}', '{}', '{}', '{}');".format(company_name, company_address, company_scale, company_desc)
        try:
            self.c.execute(sql)
        except sqlite3.IntegrityError:
            # 计数器
            self.company_repeat_error += 1
            sql = "select id from companies where company_name = '{}';".format(company_name)
            company_id = self.c.execute(sql).fetchone()[0]
        except Exception as e:
            print(e)
        else:
            # 计数器
            self.new_company_num += 1
            sql = "select max(id) from companies;"
            company_id = self.c.execute(sql).fetchone()[0]
        # 插入数据到职位数据表 并获取该条目的id
        sql = "insert into jobs(job_name, job_desc) " \
              "values('{}', '{}');".format(job_name, job_desc)
        try:
            self.c.execute(sql)
        except Exception as e:
            print(e)
        else:
            self.new_job_num += 1
            sql = "select max(id) from jobs;"
            job_id = self.c.execute(sql).fetchone()[0]
        # 确定权重
        self.glock.acquire()
        self.weight = 0
        if company_scale == '50' or company_scale == '100':
            self.weight += 1
        weight_add = [word in company_desc for word in self.c_desc_with_words]
        weight_add2 = [word in job_desc for word in self.job_desc_with_words]
        weight_min = [word in company_desc for word in self.c_desc_without_words] + [word in job_desc for word in self.job_desc_without_words]
        self.weight += (weight_add.count(True) + weight_add2.count(True)*5 - weight_min.count(True))
        # 插入爬取数据表数据
        sql = "insert into raw_datas(area_id, company_id, job_id, weight) " \
              "values({}, {}, {}, {});".format(self.area_id, company_id, job_id, self.weight)

        self.total += 1
        self.c.execute(sql)
        self.conn.commit()
        self.glock.release()
        return

    def set_area_id(self):
        self.area_id = ''
        # 插入数据到区域表 并获取该区域的id
        sql = "insert into areas(area) values('{}');".format(self.city)
        try:
            self.c.execute(sql)
        except sqlite3.IntegrityError:
            sql = "select id from areas where area = '{}';".format(self.city)
            self.area_id = self.c.execute(sql).fetchone()[0]
        except Exception as e:
            print(type(e))
        else:
            sql = "select max(id) from areas;"
            self.area_id = self.c.execute(sql).fetchone()[0]
        self.conn.commit()

    def close(self, spider, reason):
        print('公司重复次数')
        print(self.company_repeat_error)
        print('指纹重复次数')
        print(self.fingerprint_repeat_error)
        print('插入数据总数')
        print(self.total)
        print('新工作数\n', self.new_job_num, sep='')
        print('新公司数\n', self.new_company_num, sep='')
