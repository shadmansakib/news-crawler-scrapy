
from datetime import datetime

from crawler.items import NewsLoader, NewsItem
from pytz import timezone
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule

class BdnewsLoader(NewsLoader):
    # convert "14 Jul 2020 02:29 PM BdST" format datetime string to datetime object
    # For adding timezone,
    # See : https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python
    publish_time_in = MapCompose(
        lambda t: datetime.strptime(t.strip(), "%d %b %Y %I:%M %p BdST"),
        lambda t: timezone("Asia/Dhaka").localize(t)
    )

    last_update_time_in = MapCompose(
        lambda t: datetime.strptime(t.strip(), "%d %b %Y %I:%M %p BdST"),
        lambda t: timezone("Asia/Dhaka").localize(t)
    )


class BdnewsSpider(CrawlSpider):
    name = 'bdnews'
    allowed_domains = ['bdnews24.com']
    start_urls = ['https://bangla.bdnews24.com/news/']

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=r'//li/div[contains(@class, "articleTitle")]/a[1]'
            ),
            callback='parse_news'
        ),

    )

    def parse_news(self, response):
        loader = BdnewsLoader(item=NewsItem(), response=response)

        loader.add_xpath(
            'heading',
            '//h1[contains(@class,"print-only")]/text()'
        )

        loader.add_xpath(
            'author',
            '//p[contains(@class,"byline")]/text()'
        )

        loader.add_xpath(
            'publish_time',
            '//span[contains(text(), "Published:")]/following-sibling::span[1]/text()'
        )

        loader.add_xpath(
            'last_update_time',
            '//span[contains(text(), "Updated:")]/following-sibling::span[1]/text()'
        )

        loader.add_xpath(
            'details',
            '//h5[contains(@class, "print-only")]/text()'
        )    # first paragraph

        loader.add_xpath(
            'details',
            '//div[contains(@class,"wrappingContent")]/descendant-or-self::p/text()'
        )

        # kids section
        loader.add_xpath(
            'details',
            '//div[contains(@class, "custombody")]/p/descendant-or-self::*/text()'
        )

        loader.add_xpath(
            'categories',
            '//div[contains(@class, "navigation")]/a[last()]/text()'
        )    # category

        loader.add_xpath(
            'tags',
            '//div[contains(@class, "navigation")]/a[last()]/text()'
        )  # add category to tags


        loader.add_xpath(
            'tags',
            '//div[contains(@class, "tagNames")]/a/text()'
        )    # tags

        loader.add_xpath(
            'image',
            '//div[contains(@class, "print-only")]/div[@class="media"]/img[1]/@src'
        )

        loader.add_xpath(
            'excerpt',
            '//h5[contains(@class, "print-only")]/text()'
        )    # this is also the first paragraph of details

        loader.add_value(
            'news_url',
            response.url
        )

        loader.add_value(
            'publisher',
            'বিডিনিউজ টোয়েন্টিফোর ডটকম'
        )

        loader.add_value(
            'language',
            'bn'
        )

        return loader.load_item()
