# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['http://blog.jobbole.com/']
    start_urls = ['http://blog.jobbole.com/114505/']

    def parse(self, response):
        req = response.xpath('//*[@id="post-114505"]/div[1]/h1/text()').extract()[0]
        pass
