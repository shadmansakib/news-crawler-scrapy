from datetime import datetime

from crawler.items import NewsLoader, NewsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule


class PaloNewsLoader(NewsLoader):
    categories_in = MapCompose(lambda item: item.replace(u'সংবাদ', '').strip())

    # convert timezone aware string "2020-07-14T12:37:00+06:00" to datetime object
    publish_time_in = MapCompose(lambda item: datetime.fromisoformat(item))
    last_update_time_in = MapCompose(lambda item: datetime.fromisoformat(item))


class ProthomaloSpider(CrawlSpider):
    name = 'prothomalo'
    allowed_domains = ['prothomalo.com']
    start_urls = ['https://prothomalo.com/archive']

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=r'//div[contains(@class, "each")]/a[@class="link_overlay"]'
            ),
            callback='parse_news',
        ),

        # follow pagination
        Rule(
            LinkExtractor(allow=r'/?page=[0-9]+'),
            follow=True,
        ),
    )

    def parse_news(self, response):
        loader = PaloNewsLoader(item=NewsItem(), response=response)

        loader.add_xpath(
            'heading',
            '//div[@class="right_title"]/h2[contains(@class, "subtitle")]/text()'
        )

        loader.add_xpath(
            'heading',
            '//div[@class="right_title"]/h1[contains(@class, "title")]/text()'
        )

        loader.add_xpath(
            'author',
            '//div[contains(@class, "author")]/span[@class="name"]/text()'
        )

        loader.add_xpath(
            'publish_time',
            '//div[@class="additional_info_container"]/div[contains(@class, "time")]/span[@itemprop="datePublished"]/@content'
        )

        loader.add_xpath(
            'last_update_time',
            '//div[@class="additional_info_container"]/div[contains(@class, "time")]/span[@itemprop="dateModified"]/@content'
        )

        loader.add_xpath(
            'details',
            '//article[contains(@class, "content")]/descendant-or-self::p/text()'
        )

        loader.add_xpath(
            'tags',
            '//div[@class="topic_list"]/a/strong/text()'
        )

        loader.add_xpath(
            'image',
            '//article//img/@src'
        )

        loader.add_xpath(
            'categories',
            '//div[@class="left_category"]/div[@class="col_in"]/a[@class="category_name"]/text()'
        )

        loader.add_xpath(
            'excerpt',
            '//meta[@name="description"]/@content'
        )

        loader.add_value(
            'news_url',
            response.url
        )

        loader.add_value(
            'publisher',
            'প্রথম আলো'
        )

        loader.add_value(
            'language',
            'bn'
        )

        return loader.load_item()
