# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from functools import reduce
import re
import scrapy
import requests
from lxml import etree
from ..items import TargetCompanyItem
from hashlib import md5
import sqlite3


class A51jobSpider(scrapy.Spider):
    name = 'job51'
    allowed_domains = ['51job.com']
    def __init__(self):
        super(A51jobSpider, self).__init__()
        self.i = 0
        self.start_url = 'https://search.51job.com/list/{},000000,0000,00,9,99,{},2,{}.html'
        self.keyword = input('输入要搜索的职位关键词: ')
        self.city = input('请输入城市: ')
        self.city_code = {'杭州':'080200','义乌':'081400','金华':'080600'}
        # 连接数据库
        self.conn = sqlite3.connect('target_company.db')
        self.c = self.conn.cursor()
        sql = 'select id from areas where area="{}";'.format(self.city)
        try:
            self.city_id = self.c.execute(sql).fetchone()[0]
        except Exception as e:
            raise(e)
            sql = 'insert into areas(area) values("{}");'.format(self.city)
            self.c.execute(sql)
            sql = 'select max(id) from areas;'
            self.city_id = self.c.execute(sql).fetchone()[0]
        finally:
            self.conn.commit()

    def start_requests(self):
        header = {
            'Cookie': 'guid=49792de30478139ba4dfec538eae9378; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; partner=www_baidu_com; _ujz=MTQwNzcwNzY5MA%3D%3D; slife=lowbrowser%3Dnot%26%7C%26lastlogindate%3D20200426%26%7C%26; ps=needv%3D0; 51job=cuid%3D140770769%26%7C%26cusername%3Dphone_13735385294%26%7C%26cpassword%3D%26%7C%26cname%3D%25D6%25EC%25D6%25BE%25C5%25F4%26%7C%26cemail%3Daugustaosh%2540163.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0PatVJRmR83o%26%7C%26cconfirmkey%3Dau4NgaiBuHXZA%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3DaulYMktwZI.ck%26%7C%26to%3Dcc165bafeb9cfae5dbbac4e30aff81075ea51590%26%7C%26; search=jobarea%7E%60080200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60080200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60080200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%CD%E2%C3%B3%D7%A8%D4%B1%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%CD%E2%C3%B3%D7%A8%D4%B1%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21collapse_expansion%7E%601%7C%21',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        }
        params = dict(lang='c', stype='', postchannel='0000', workyear='99', cotype='99', degreefrom='99', jobterm='99',
                      companysize='99', providesalary='99', lonlat='0, 0', radius='-1', ord_field='0', confirmdate='9',
                      fromType='', dibiaoid='0', specialarea='00', address='', line='', werlare='')
        response = requests.get(url=self.start_url.format(self.city_code[self.city],self.keyword, 1), headers=header, params=params)
        html = etree.HTML(response.content.decode(encoding='gbk'))
        urls = self.get_index_page_url(html)
        while urls:
            response = requests.get(url=urls.pop(), headers=header, params=params)
            html = etree.HTML(response.content.decode(encoding='gbk'))
            job_urls = html.xpath('//div[contains(@class,"dw_table")]//div[contains(@class,"el") and position()>3]//p//a/@href')
            for job_url in job_urls:
                # 增量爬虫
                url_md5 = job_url.split('?')[0]
                self.fingerprint = md5(url_md5.encode(encoding='utf-8')).hexdigest()
                sql = 'insert into fingerprint values("{}");'.format(self.fingerprint)
                try:
                    self.c.execute(sql)
                except sqlite3.IntegrityError:
                    continue
                except Exception as e:
                    raise (e)
                else:
                    self.conn.commit()
                    yield scrapy.Request(url=job_url, callback=self.parse)

    def parse(self, response):
        job_name = response.xpath('//div[@class="cn"]/h1/@title').get()
        c_name = response.xpath('//div[@class="cn"]/p[@class="cname"]/a/@title').get()
        c_scale = response.xpath('//div[@class="com_tag"]/p[2]/@title').get()
        c_industry = response.xpath('//div[@class="com_tag"]/p[3]/@title').get()
        c_addr = response.xpath('//div[@class="bmsg inbox"]/p/text()').get()
        job_desc = response.xpath('//div[@class="bmsg job_msg inbox"]//text()').extract()
        c_desc = response.xpath('//div[@class="tmsg inbox"]/text()').extract()
        item = TargetCompanyItem()
        item['job_url'] = response.url
        item['job_name'] = job_name
        item['c_name'] = c_name
        item['c_scale'] = c_scale
        item['c_industry'] = c_industry
        item['c_addr'] = c_addr
        try:
            item['job_desc'] = reduce(lambda x, y: x + y, job_desc).replace("'", "")
        except Exception as e:
            raise DropItem('岗位详情没有,DropItem')
        try:
            item['c_desc'] = reduce(lambda x, y: x + y, c_desc).replace("'", "")
        except Exception as e:
            raise e
        try:
            item['weight'] = self.get_weight(job_desc, c_desc, c_name)
        except TypeError:
            pass
        # item['url_fingerprint'] = url_fingerprint
        self.i += 1
        return item

    def get_index_page_url(self, html):
        nums_text = html.xpath('//span[@class="td"][1]/text()')
        pattern = re.compile(r'共(.*?)页')
        total_num = int(pattern.findall(nums_text[0])[0])
        tmp = []
        for i in range(1, total_num + 1):
            url = self.start_url.format(self.city_code[self.city],self.keyword, i)
            tmp.append(url)
        return tmp

    @staticmethod
    def get_weight(job_desc, c_desc, c_name):
        weight = 0
        c_name_without_words = '厂 工贸 制品 用品 制造'.split(' ')
        c_desc_with_words_2 = '外贸 跨境 贸易 中小额 批发 零售 进出口'.split(' ')
        job_desc_with_words_3 = ' excel 数据 售前 编写商品 产品编码 表格 新品 编码 erp ERP Excel'.split(' ')
        if True in [word in c_name for word in c_name_without_words]:
            return False
        weight += [word in c_desc for word in c_desc_with_words_2].count(True)*2
        weight += [word in job_desc for word in job_desc_with_words_3].count(True)*3
        return weight

    def get_from_list(self, thing):
        if type(thing) == 'list':
            return thing[0]
        else:
            return thing

    def close(spider, reason):
        print('爬取数据:{}条'.format(spider.i))