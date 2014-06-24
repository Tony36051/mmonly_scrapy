# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MmonlyItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

    link = Field()
    number = Field()
    title = Field()
    update_time = Field()
    description = Field()
    category = Field()
    pages = Field()
    image_urls = Field()
    image_paths = Field()
    images = Field()
    path = Field()
    state = Field()#'ok' or 'fail'
    
