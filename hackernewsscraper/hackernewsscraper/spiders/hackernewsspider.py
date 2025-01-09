import scrapy
from hackernewsscraper.items import HackernewsscraperItem
from hackernewsscraper.itemloaders import HackerNewsLoader

class HackernewsspiderSpider(scrapy.Spider):
    name = "hackernewsspider"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ["https://news.ycombinator.com"]

    def parse(self, response):
        # table = response.xpath('//table[@id="hnmain"]/tr[3]/td/table/tr')
        title_url_selector = response.css('span.titleline')
        subdata_selector = response.css('td.subtext')

        # print(len(title_url_selector))
        # print(len(subdata_selector))

        for i in range(len(title_url_selector)):
            
            item_loader = HackerNewsLoader(item=HackernewsscraperItem(), selector=title_url_selector[0])
            
            item_loader.selector = title_url_selector[i]
            item_loader.add_css('title', 'a::text')
            item_loader.add_css('url', 'a::attr(href)')

            item_loader.selector = subdata_selector[i]
            item_loader.add_css('points', 'span.score::text', re='\d+')
            item_loader.add_css('username', 'a.hnuser::text')
            item_loader.add_css('comments', 'a:nth-of-type(3)::text', re='\d+')
            item_loader.add_css('date', 'span.age::attr(title)')

            yield item_loader.load_item()

            next_page_url = response.css('a.morelink::attr(href)').get()
            # print(next_page_url)
            if next_page_url is not None:
                next_page_url = 'https://news.ycombinator.com/' + next_page_url
                yield response.follow(next_page_url, callback=self.parse)
