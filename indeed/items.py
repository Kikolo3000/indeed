# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title       = scrapy.Field(serializer=str)
    company     = scrapy.Field(serializer=str)
    address     = scrapy.Field(serializer=str)
    description = scrapy.Field(serializer=str)
    #salary      = scrapy.Field(serializer=str)
 
    pass
