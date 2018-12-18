# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SimilarAppScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    App_Name = scrapy.Field()
    #App_Category = scrapy.Field()
    App_ID = scrapy.Field()
    App_Image_Name = scrapy.Field()
    App_Icon_URL = scrapy.Field()
