# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SchoolInfo(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    keywords=scrapy.Field()
    depth=scrapy.Field()
    link=scrapy.Field()
    school=scrapy.Field()
    previous=scrapy.Field()
