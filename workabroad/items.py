# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WorkabroadItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class PostItem(Item):
    href = Field()
    id = Field()
    title = Field()
    location = Field()
    expiry = Field()
    agency = Field()
    qualifications = Field()
    info = Field()
    requirements = Field()
