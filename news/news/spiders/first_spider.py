import scrapy
import news_api.db as db
from news import items


class UnianSpider(scrapy.Spider):
    name = 'unian'

    def start_requests(self):
        urls = [
            'https://www.pravda.com.ua/news/2022/02/1/7322400/',
            'https://www.unian.ua/politics/dbr-provodit-obshuki-u-kolishnogo-golovi-naftogazu-kobolyeva-dbr-novini-ukrajina-11689753.html',
            'https://www.ukrinform.ua/rubric-polytics/3393674-kremlivskij-milnij-serial-novi-suzeti-z-neasnim-finalom.html',
            'https://lenta.ua/polyarnaya-noch-ili-kratkovremennoe-zatmenie-zachem-zelenskiy-rugaetsya-s-baydenom-115114/'
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

        item['url'] = url
        item['title'] = title
        item['date'] = news_date
        item['author'] = author
        item['author_link'] = author_link
        item['short'] = short
        item['main_text'] = main_text
        yield item
