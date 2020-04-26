# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import etree


class A51jobSpider(scrapy.Spider):
    name = 'job51'
    allowed_domains = ['51job.com']
    start_url = 'https://search.51job.com/list/080200,000000,0000,00,9,99,{},2,1.html'

    def start_requests(self):
        keyword = input('输入要搜索的职位关键词: ')
        header = {
            'Cookie': 'guid=49792de30478139ba4dfec538eae9378; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; partner=www_baidu_com; _ujz=MTQwNzcwNzY5MA%3D%3D; slife=lowbrowser%3Dnot%26%7C%26lastlogindate%3D20200426%26%7C%26; ps=needv%3D0; 51job=cuid%3D140770769%26%7C%26cusername%3Dphone_13735385294%26%7C%26cpassword%3D%26%7C%26cname%3D%25D6%25EC%25D6%25BE%25C5%25F4%26%7C%26cemail%3Daugustaosh%2540163.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0PatVJRmR83o%26%7C%26cconfirmkey%3Dau4NgaiBuHXZA%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3DaulYMktwZI.ck%26%7C%26to%3Dcc165bafeb9cfae5dbbac4e30aff81075ea51590%26%7C%26; search=jobarea%7E%60080200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60080200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60080200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%CD%E2%C3%B3%D7%A8%D4%B1%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%CD%E2%C3%B3%D7%A8%D4%B1%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21collapse_expansion%7E%601%7C%21',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        }
        params = dict(lang='c', stype='', postchannel='0000', workyear='99', cotype='99', degreefrom='99', jobterm='99',
                      companysize='99', providesalary='99', lonlat='0, 0', radius='-1', ord_field='0', confirmdate='9',
                      fromType='', dibiaoid='0', specialarea='00', address='', line='', werlare='')
        response = requests.get(url=self.start_url.format(keyword), headers=header, params=params)
        print(response.url)
        html = etree.HTML(response.content.decode(encoding='gbk'))
        print(html.xpath('//div[contains(@class,"dw_table")]//div[contains(@class,"el") and position()>3]//p//a/@title | '
                         '//div[contains(@class,"dw_table")]//div[contains(@class,"el") and position()>3]//p//a/@href'))
        yield None