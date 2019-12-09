# -*- coding: utf-8 -*-
import scrapy
from ..items import *
import json


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    # start_urls = ['http://careers.tencent.com/']
    # index=1

    def start_requests(self):
        keyword=input('请输入类型:')
        one_url='https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1574335458669&countryId=&cityId' \
                '=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={' \
                '}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        url=one_url.format(keyword,1)
        yield scrapy.Request(
            url=url,
            callback=self.get_total,
            meta={'keyword':keyword,'one_url':one_url}
            )


    def get_total(self, response):
        one_url = response.meta['one_url']
        html=json.loads(response.text)
        count=int(html['Data']['Count'])
        if count%10==0:
            total=count//10
        else:
            total=count//10+1
        keyword=response.meta['keyword']
        for index in range(1,total+1):
            url=one_url.format(keyword,index)
            yield  scrapy.Request(
                url=url,
                callback=self.parse_one_page,
                meta={'keyword': keyword, 'one_url': one_url}
            )


        # meta = {'item': item}
        # item = TencentItem()

    def parse_one_page(self, response):
        while True:
            item = TencentItem()
            html = json.loads(response.text)
            for data in html['Data']['Posts']:
                post_id = data['PostId']
                two_url = self.two_url.format(post_id)
                self.two_q.put(two_url)


        pass
