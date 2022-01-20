import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from news.items import NewsItem

class UnianSpider(scrapy.Spider):
    name = 'unian'

    def start_requests(self):
        urls = [
            'https://health.unian.net/health/koronavirus-nabiraet-oboroty-za-sutki-zarazilis-pochti-13-tysyach-ukraincev-11675953.html',
            'https://health.unian.net/health/vse-ochen-prosto-doktor-komarovskiy-otvetil-na-populyarnyy-vopros-o-privivkah-11675938.html',
            'https://health.unian.net/health/kak-pravilno-kupatsya-na-kreshchenie-2022-v-minzdrave-dali-sovety-11675716.html'
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = NewsItem()
        title = response.css('div.article:nth-child(1) > h1:nth-child(2)').getall()
        date = response.css('div.article__info-item.time:nth-child(2)').get()
        short = response.css('p.article__like-h2:nth-child(4)').get()
        text = response.css('div.article-text > p').getall()
        author = response.css('a.article__author-name').get()
        item['title'] = title
        item['short'] = short
        item['date'] = date
        item['author'] = author
        item['main_text'] = text
        yield item
