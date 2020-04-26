# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import json
from scrapy.exceptions import DropItem


class TargetCompanyPipeline(object):

    def open_spider(self, spider):
        """爬虫开始时执行一次，链接数据库"""
        self.conn = sqlite3.connect('target_company.db')
        print('连接数据库')
        self.c = self.conn.cursor()

    def process_item(self, item, spider):
        if item['weight'] is False:
            raise DropItem("Item not good {}".format(item['weight']))
        # 插入数据到公司信息表 并获取该条目的id
        sql = "insert into companies(company_name, company_address, company_scale, company_desc)" \
              "values('{}', '{}', '{}', '{}');".format(item['c_name'], item['c_addr'], item['c_scale'], item['c_desc'])
        try:
            self.c.execute(sql)
        except sqlite3.IntegrityError:
            sql = "select id from companies where company_name = '{}';".format(item['c_name'])
            c_id = self.c.execute(sql).fetchone()[0]
        else:
            sql = "select max(id) from companies;"
            c_id = self.c.execute(sql).fetchone()[0]
        # 插入数据到职位数据表 并获取该条目的id
        sql = "insert into jobs(job_name, job_desc) " \
              "values('{}', '{}');".format(item['job_name'], item['job_desc'])
        self.c.execute(sql)
        sql = "select max(id) from jobs;"
        job_id = self.c.execute(sql).fetchone()[0]
        # 插入爬取数据表数据
        sql = "insert into raw_datas(area_id, company_id, job_id, weight) " \
              "values({}, {}, {}, {});".format(spider.city_id, c_id, job_id, item['weight'])
        self.c.execute(sql)
        self.conn.commit()
        return item
