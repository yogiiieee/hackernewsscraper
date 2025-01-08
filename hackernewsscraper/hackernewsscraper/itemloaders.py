from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst

class HackerNewsLoader(ItemLoader):
    default_output_processor = TakeFirst()