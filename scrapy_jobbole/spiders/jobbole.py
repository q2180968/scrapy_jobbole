# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from scrapy_jobbole.items import AtricleItem
from scrapy_jobbole.utils import *


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    # allowed_domains = ['http://blog.jobbole.com/all-posts/']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # 爬虫主程序
    def parse(self, response):
        '''
        1、获取文章列表中的文章url并且交给scrapy下载后进行解析
        2、获取下一页url并且交给scrapy进行下载，下载完成后再交给parse
        '''
        # 获取爬取路径节点
        post_nodes = response.css('#archive  .floated-thumb .post-thumb a')
        # 循环节点，获取需要爬取路径和缩略图
        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first('')
            url = post_node.css('::attr(href)').extract_first('')
            # 通过yield生成器开始爬取，callback调取详情页提取数据
            yield Request(url=parse.urljoin(response.url, url), meta={'front_image_url': image_url},
                          callback=self.parse_detail)

        # 获取下一页url
        next_url = response.css('.next::attr(href)').extract_first('')
        next_url = parse.urljoin(response.url, next_url)
        # 如果有下一页，通过yield生成器传递给主程序，循环爬取下一页
        if next_url:
            # yield Request(url=next_url, callback=self.parse)
            pass

    # 详情页数据提取
    def parse_detail(self, response):

        article = AtricleItem()
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
        article['title'] = title
        article['url'] = response.url
        article['url_object_id'] = getHash(response.url)
        article['create_date'] = pub_time
        article['front_image_url'] = [response.meta['front_image_url']]
        article['comment'] = comment
        article['collection'] = collection
        article['enjoy'] = enjoy

        yield article
