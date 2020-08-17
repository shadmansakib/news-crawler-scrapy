from datetime import datetime

from crawler.items import NewsLoader, NewsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule


class DailystarBd_En_NewsLoader(NewsLoader):
    # convert timezone aware string "2020-08-17T17:32:00+06:00" to datetime object
    publish_time_in = MapCompose(lambda item: datetime.fromisoformat(item))
    last_update_time_in = MapCompose(lambda item: datetime.fromisoformat(item))



class DailystarBdEnSpider(CrawlSpider):
    name = 'dailystar_bd_en'
    allowed_domains = ['thedailystar.net']
    start_urls = ['https://www.thedailystar.net/online']

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=r'//li/h4[@class="pad-bottom-small"]/a'
            ),
            callback='parse_news'
        ),

        # follow pagination
        Rule(
            LinkExtractor(
                # allow=r'/online?page=[0-9]+'
                restrict_xpaths=r'//li[contains(@class, "pager-show-more-next")]/a'
            ),
            follow=True,
        ),
    )

    def parse_news(self, response):
        loader = DailystarBd_En_NewsLoader(item=NewsItem(), response=response)

        loader.add_xpath(
            'heading',
            '//h1[@itemprop="headline"]/text()'
        )

        loader.add_xpath(
            'author',
            '//div[contains(@class, "author-name")]/span[@itemprop="name"]/text()'
        )

        loader.add_xpath(
            'publish_time',
            '//meta[@itemprop="datePublished"]/@content'
        )

        loader.add_xpath(
            'last_update_time',
            '//meta[@itemprop="dateModified"]/@content'
        )

        loader.add_xpath(
            'details',
            '//div[@class="node-content"]/descendant-or-self::p/strong/text()'
        )    # first paragraph

        loader.add_xpath(
            'details',
            '//div[@class="node-content"]/descendant-or-self::p/text()'
        )

        # Tags and categories are same for this site
        loader.add_xpath(
            'tags',
            '//div[@class="breadcrumb"]/span[@itemprop="itemListElement"][last()]/descendant-or-self::a/span/text()'
        )
        loader.add_xpath(
            'image',
            '//img[@class="image-style-big-2"]/@src'
        )

        loader.add_xpath(
            'categories',
            '//div[@class="breadcrumb"]/span[@itemprop="itemListElement"][last()]/descendant-or-self::a/span/text()'
        )

        loader.add_xpath(
            'excerpt',
            '//meta[@itemprop="description"]/@content'
        )

        loader.add_value(
            'news_url',
            response.url
        )

        loader.add_value(
            'publisher',
            'The Daily Star'
        )

        loader.add_value(
            'language',
            'en'
        )

        return loader.load_item()
