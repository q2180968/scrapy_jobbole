# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyJobboleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AtricleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    create_date = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    comment = scrapy.Field()
    collection = scrapy.Field()
    tags = scrapy.Field()
    enjoy = scrapy.Field()
    # content = scrapy.Field()
