# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import re
from datetime import datetime


# 重载ItemLoader，把List变成第一个输出
class AtricleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ScrapyJobboleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 时间格式化处理
def datetime_filter(value):
    value = value.strip().replace('·', '').strip()
    try:
        create_date = datetime.strptime(value, '%Y%M%D').date()
    except Exception as e:
        create_date = datetime.now().date()
    return create_date


# 取值中的数字
def num_filter(value):
    pattern = r'.*?(\d+).*?'
    match_re = re.match(pattern, value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


# 图片仍然为列表输出方法
def img_filter(value):
    return value


# tag去掉评论
def tag_filter(value):
    if '评论' in value:
        return ""
    else:
        return value


class AtricleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(datetime_filter)
    )
    front_image_url = scrapy.Field(
        output_processor=MapCompose(img_filter)
    )
    front_image_path = scrapy.Field()
    comment = scrapy.Field(
        input_processor=MapCompose(num_filter)
    )
    collection = scrapy.Field(
        input_processor=MapCompose(num_filter)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=Join(',')
    )
    enjoy = scrapy.Field(
        input_processor=MapCompose(num_filter)
    )
    content = scrapy.Field()
