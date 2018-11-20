# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['http://blog.jobbole.com/']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1、获取文章列表中的文章url并且交给scrapy下载后进行解析
        2、获取下一页url并且交给scrapy进行下载，下载完成后再交给parse
        '''
        post_urls = response.css('#archive  .floated-thumb .post-thumb a::attr(href)').extract()
        for post_url in post_urls:
            url = parse.urljoin(response.url, post_url)
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

        pass

    def parse_detail(self, response):
        # 获取标题
        title = response.css('.entry-header h1::text').extract_first('')
        # 获取发布时间
        pub_time = response.css('.entry-meta-hide-on-mobile::text').extract_first('').strip().replace('·', '').strip()
        # 获取tag
        tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [emelent for emelent in tag_list if not emelent.strip().endswith('评论')]
        # 获取内容
        content = response.css('.entry').extract()
        # 获取点赞数
        enjoy = response.css('.vote-post-up h10::text').extract_first('')
        if enjoy == '':
            enjoy = 0
        else:
            enjoy = int(enjoy)
        # 获取收藏数
        collection = response.css('.bookmark-btn::text').extract_first('')
        pattern = r'.*?(\d+).*?'
        match_re = re.match(pattern, collection)
        if match_re:
            collection = int(match_re.group(1))
        else:
            collection = 0
        # 获取评论数
        comment = response.css('a[href="#article-comment"] span::text').extract_first('')
        match_re = re.match(pattern, comment)
        if match_re:
            comment = int(match_re.group(1))
        else:
            comment = 0
        pass
