# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from db.models import News
from db.mongo import init_db
# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem


class DiscardUnsupported:
    def process_item(self, item, spider):
        if not item.get("details"):
            raise DropItem('>>> [DROP] Item has no details attribute')
        return item


class SaveNews:
    def __init__(self):
        # init db
        init_db()

    def process_item(self, news_item, spider):
        news = News(**news_item)
        try:
            news.save()
        except Exception as e:
            raise DropItem('>>> [SAVE ERROR] cannot save news : {}'.format(e))
        return news_item


