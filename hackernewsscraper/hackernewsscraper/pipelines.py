# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import json
import os
from dotenv import load_dotenv
from database.models import News  # Adjusted import statement
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

load_dotenv()

class HackernewsscraperPipeline:
    def process_item(self, item, spider):
        return item


class ExtractCountAndDatePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        adapter['points'] = int(adapter.get('points', 0))
        adapter['comments'] = int(adapter.get('comments', 0))

        if adapter.get('date'):
            adapter['date'] = adapter['date'][:10]

        return item


class HandleMissingSubdataPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if not adapter.get('username'):
            adapter['username'] = None
        
        if not adapter.get('date'):
            adapter['date'] = None

        return item


class JSONFormatterPipeline:
    def open_spider(self, spider):
        self.formatted_data = {}

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if item:
            self.formatted_data[adapter['title']] = {
                'url': adapter['url'],
                'points': adapter['points'],
                'username': adapter['username'],
                'comments': adapter['comments'],
                'date': adapter['date']
            }
        
    def close_spider(self, spider):
        with open('output.json', 'w') as file:
            json.dump(self.formatted_data, file, indent=4, ensure_ascii=False)


class PostgresDBPipeline:
    def __init__(self):
        self.engine = create_engine(os.getenv('DATABASE_URL'))
        self.Session = sessionmaker(bind=self.engine)
        # self.Session = Session

    def process_item(self, item, spider):
        session = self.Session()
        meta_data = {
            'comments': item['comments'],
            'points': item['points']
        }

        existing_post = session.query(News).filter(News.title == item['title']).first()
        if existing_post:
            existing_post.meta = meta_data
        else:
            news_post = News(
                title = item['title'],
                url = item['url'],
                username = item['username'],
                date = datetime.strptime(item['date'], '%Y-%m-%d').date(),
                meta = meta_data
            )

            session.add(news_post)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            spider.logger.error(f'Error uploading to db: {e}')
        finally:
            session.close()      
        return item