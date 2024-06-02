import scrapy
from ..items import Product_Item  # Adjusted to use relative import

class BlackboxSpiderSpider(scrapy.Spider):
    name = "blackbox_spider"
    allowed_domains = ["blackbox.com.sa"]
    start_urls = ['https://blackbox.com.sa/en/smartphones-tablets.html',
                  'https://blackbox.com.sa/en/tv.html',
                  'https://blackbox.com.sa/en/air-conditioners-accessories.html',
                  'https://blackbox.com.sa/en/large-appliances.html',
                  'https://blackbox.com.sa/en/kitchen-appliances/small-appliances.html',
                  'https://blackbox.com.sa/en/computer-accessories.html',
                  'https://blackbox.com.sa/en/gaming.html',
                  'https://blackbox.com.sa/en/personal-care.html']

    categories = {
        'https://blackbox.com.sa/en/smartphones-tablets.html': 'Smartphones & Tablets',
        'https://blackbox.com.sa/en/tv.html': 'TV',
        'https://blackbox.com.sa/en/air-conditioners-accessories.html': 'Air Conditioners & Accessories',
        'https://blackbox.com.sa/en/large-appliances.html': 'Large Appliances',
        'https://blackbox.com.sa/en/kitchen-appliances/small-appliances.html': 'Small Kitchen Appliances',
        'https://blackbox.com.sa/en/computer-accessories.html': 'Computer Accessories',
        'https://blackbox.com.sa/en/gaming.html': 'Gaming',
        'https://blackbox.com.sa/en/personal-care.html': 'Personal Care'
    }

    def parse(self, response):
        items = response.css('div.item-inner')
        category = self.categories[response.url]

        for item in items:

            product_url = item.css('.product-item-name .product-item-link::attr(href)').get()

            if product_url:
                self.log(f'Next page URL: {product_url}')
                yield response.follow(product_url, callback=self.parse_product_page, meta={'category': category})
            else:
                self.log('No more pages to crawl.')



    def parse_product_page(self, response):
        category = response.meta['category']

        item = Product_Item()  # Instantiate the item

        def extract_with_css(query):
            return response.css(query).get(default='Not available').strip()

        item['category'] = category
        item['was_price'] = extract_with_css(
            "div.price-box.price-final_price span.old-price span.price-wrapper span.price::text")
        item['price'] = extract_with_css(
            "div.price-box.price-final_price span.special-price span.price-wrapper span.price::text")
        item['url'] = response.url
        item['thumbnail_url'] = extract_with_css('div.fotorama__stage__frame::attr(href)')
        item['brand'] = extract_with_css("td.col.data[data-th='Brand']::text")
        item['product_id'] = extract_with_css("td.col.data[data-th='Model Number']::text")

        yield item


