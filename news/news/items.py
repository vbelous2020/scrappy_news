# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class NewsItem(Item):
    url = Field()
    title = Field()
    date = Field()
    timestamp = Field()
    author = Field()
    author_link = Field()
    short = Field()
    main_text = Field()
    cleared = Field()

