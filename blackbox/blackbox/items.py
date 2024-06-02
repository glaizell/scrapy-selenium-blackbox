# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BlackboxItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass



class Product_Item(scrapy.Item):
    category = scrapy.Field()
    was_price = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    thumbnail_url = scrapy.Field()
    brand = scrapy.Field()
    product_id = scrapy.Field()