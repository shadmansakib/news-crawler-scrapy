# See: https://docs.scrapy.org/en/latest/topics/api.html
# See: https://www.programmersought.com/article/52891569185/


from crawler.spiders.prothomalo import ProthomaloSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    # process = CrawlerProcess({
    #     'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 RuxitSynthetic/1.0 v5298915840 t38550'
    # })

    process = CrawlerProcess(get_project_settings())

    # spiders
    process.crawl(ProthomaloSpider)

    process.start()


if __name__ == '__main__':
    main()
