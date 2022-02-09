from datetime import datetime
import pytz
import scrapy
import news_api.db as db
from .. import items


class UnianSpider(scrapy.Spider):
    name = 'unian'

    def start_requests(self):
        urls = [
            'https://www.pravda.com.ua/news/2022/02/8/7323171/',
            'https://www.unian.ua/politics/zustrich-zelenskogo-i-makrona-u-kiyevi-8-lyutogo-onlayn-translyaciya-na-unian-detali-zahodu-novini-ukrajina-11696944.html',
            'https://www.ukrinform.ua/rubric-economy/3398196-rinok-palnogo-lihomanit-ci-zmozut-ukrainci-zapraviti-svoi-avto-za-novimi-cinami.html',
            'https://lenta.ua/kreml-davit-kakoy-dolzhna-byt-reaktsiya-ukrainy-115556/'
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = items.NewsItem()
        url = response.request.url
        print(f"Url: {response.request.url}")
        pattern = db.check_pattern(url)
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
        yield item
