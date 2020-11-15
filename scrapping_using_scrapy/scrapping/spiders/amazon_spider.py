import scrapy
from ..items import ScrappingItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    page_number = 2
    #allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.in/s?k=books&ref=nb_sb_noss_2']

    def parse(self, response):
        items = ScrappingItem()
        product_name = response.css('.a-size-medium::text').extract()
        product_author = response.css('.a-color-secondary .a-size-base+ .a-size-base').css('::text').extract()
        product_price = response.css('.a-price-whole').css('::text').extract()
        product_imagelink = response.css('.s-image::attr(src)').extract()

        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_imagelink'] = product_imagelink

        yield items

        next_page = 'https://www.amazon.in/s?k=books&page=' + str(AmazonSpiderSpider.page_number) +  '&qid=1603889933&ref=sr_pg_' + str(AmazonSpiderSpider.page_number)

        if AmazonSpiderSpider.page_number < 5:
            yield response.follow(next_page, callback = self.parse)
