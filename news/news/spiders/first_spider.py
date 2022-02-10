import logging
from datetime import datetime
import pytz
import scrapy
import news_api.db as db
from .. import items

logging.basicConfig(filename='../log/new_articles.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


class UnianSpider(scrapy.Spider):
    name = 'unian'
    urls = db.get_list_of_urls()
    def start_requests(self):
        urls = ['https://www.youtube.com']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = items.NewsItem()
        url = response.request.url
        print(f"Url: {response.request.url}")
        pattern = db.check_pattern(url)
        print(pattern)
        if pattern:
            title = response.css(pattern['title_path'] + " *::text").getall()
            news_date = response.css(pattern['date_path'] + " *::text").get()
            author = response.css(pattern['author_path'] + " *::text").get()
            author_link = response.css(pattern['author_path'] + " *::attr(href)").get()
            short = response.css(pattern['short_path'] + " *::text").get()
            main_text = response.css(pattern['main_text_path'] + " *::text").getall()
            my_date = datetime.now(pytz.timezone('Europe/Kiev'))
            item['url'] = url
            item['title'] = title
            item['date'] = news_date
            item['author'] = author
            item['author_link'] = author_link
            item['short'] = short
            item['main_text'] = main_text
            item['timestamp'] = my_date
            item['cleared'] = False
            logging_info = f"{url} has been parsed and saved to raw data."
            logging.info(logging_info)
            db.delete_parsed_url(url)
            yield item
        else:
            logging_info = f"We didn't have pattern for this {url}."
            logging.info(logging_info)
            yield
