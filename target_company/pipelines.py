# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from .settings import *
import pypinyin
from functools import reduce
import json


class TargetCompanyPipeline(object):

    def open_spider(self, spider):
        """爬虫开始时执行一次，链接数据库"""
        self.conn = sqlite3.connect('target_company.db')
        print('连接数据库')
        self.c = self.conn.cursor()
        # # 创建表
        # # 区域表 areas
        # sql = "create table areas(
        # id integer primary key autoincrement,
        # area text unique);"
        # self.c.execute(sql)
        # # 公司信息表 companies
        # sql = "create table companies(
        # id integer primary key autoincrement,
        # company_name text unique,
        # company_address text,
        # company_scale text,
        # company_desc text);"
        # self.c.execute(sql)
        # # 职位信息表 jobs
        # sql = "create table jobs(
        # id integer primary key autoincrement,
        # job_name text,
        # job_desc text);"
        # self.c.execute(sql)
        # # 爬取数据表 raw_datas
        # sql = "create table raw_datas(
        # id integer primary key autoincrement,
        # area_id int,
        # company_id int,
        # job_id int,
        # is_read int default 0,
        # foreign key(area_id) references areas(id),
        # foreign key(company_id) references companies(id),
        # foreign key(job_id) references jobs(id));"
        # self.c.execute(sql)
        # # 数据处理完毕表 final_datas
        # sql = "create table final_datas(
        # id integer primary key autoincrement,
        # possible int,
        # raw_id int,
        # foreign key(raw_id) references raw_datas(id));"
        # self.c.execute(sql)
        # # 创建职位详情页的url -md5 加密的指纹表
        # sql = 'create table fingerprint(url_md5 text unique);'
        # self.c.execute(sql)
        # self.conn.commit()
        # print('创建完成')

    def process_item(self, item, spider):

        return item
