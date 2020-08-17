# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Identity, MapCompose


class NewsLoader(ItemLoader):
    default_input_processor = MapCompose(lambda item: item.strip())
    default_output_processor = TakeFirst()

    heading_out = Join(separator=' - ')
    details_out = Join(separator='\n')

    categories_out = Identity()
    tags_out = Identity()


class NewsItem(scrapy.Item):
    heading = scrapy.Field()
    author = scrapy.Field()
    details = scrapy.Field()
    image = scrapy.Field()
    news_url = scrapy.Field()

    categories = scrapy.Field()
    tags = scrapy.Field()
    excerpt = scrapy.Field()

    publisher = scrapy.Field()
    language = scrapy.Field()

    publish_time = scrapy.Field()
    last_update_time = scrapy.Field()
