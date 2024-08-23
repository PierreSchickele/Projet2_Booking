# import os, logging, scrapy, and CrawlerProcess from scrapy.crawler
import logging
import os
import scrapy
from scrapy.crawler import CrawlerProcess

class BookingSpider(scrapy.Spider):
    # Nom du spider
    name = "projet_booking"

    list_cities = ["Mont Saint Michel",
        "St Malo",
        "Bayeux",
        "Le Havre",
        "Rouen",
        "Paris",
        "Amiens",
        "Lille",
        "Strasbourg",
        "Chateau du Haut Koenigsbourg",
        "Colmar",
        "Eguisheim",
        "Besancon",
        "Dijon",
        "Annecy",
        "Grenoble",
        "Lyon",
        "Gorges du Verdon",
        "Bormes les Mimosas",
        "Cassis",
        "Marseille",
        "Aix en Provence",
        "Avignon",
        "Uzes",
        "Nimes",
        "Aigues Mortes",
        "Saintes Maries de la mer",
        "Collioure",
        "Carcassonne",
        "Ariege",
        "Toulouse",
        "Montauban",
        "Biarritz",
        "Bayonne",
        "La Rochelle"]
    
    # Url to start your spider from 
    start_urls = ['https://www.booking.com/']

    def start_requests(self):
        for city in self.list_cities:
            search_url = f'https://www.booking.com/searchresults.fr.html?ss={city}'
            yield scrapy.Request(url=search_url, callback=self.parse, cb_kwargs={'city':city})

    # Callback function that will be called when starting your spider
    def parse(self, response, city):
        index = 0
        for info in response.xpath('//*[@data-testid="property-card"]'):
            if index >= 10:
                break
            index = index + 1
            url = info.xpath('div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/h3/a').attrib["href"]
            hotel_url = response.urljoin(url)
            yield scrapy.Request(url=hotel_url, callback=self.parse_hotel)

    def parse_hotel(self, response):
        name = response.xpath('//*[@id="hp_hotel_name"]/div/h2/text()').get()
        coord = response.xpath('//a[@id="hotel_address"]/@data-atlas-latlng').get()
        description = response.xpath('//*[@id="property_description_content"]/div/div/p[1]/text()').get()
        review = response.xpath('//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div[1]/text()').get()
        stars = len(response.xpath('//span[@data-testid="rating-squares"]/span').getall())
        
        yield {
            'hotel_url': response.url.split("?")[0],
            'name': name,
            'coord': coord,
            'description': description,
            'review': review,
            'stars': stars
        }

filename = "bookingscrap.json"

if filename in os.listdir('results/'):
    os.remove('results/' + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/126.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        './' + filename: {"format": "json"},
    }
})

process.crawl(BookingSpider)
process.start()