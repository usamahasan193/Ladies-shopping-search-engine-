# -*- coding: utf-8 -*-
import scrapy
import re

class GulahmedSpider(scrapy.Spider):
    name = 'gulahmed'
    start_urls = ['https://www.gulahmedshop.com/women?cat=698','https://www.gulahmedshop.com/women?cat=398','https://www.gulahmedshop.com/women?cat=153','https://www.gulahmedshop.com/women?cat=207']

    def parse(self, response):
        i=response.url
        cat_name={}
        if re.search("(?i)698", i):
            cat_name={"cat_name": "STITCHED FABRIC"}
        elif re.search("(?i)207", i):
            cat_name={"cat_name": "SALT"}
        elif re.search("(?i)153", i):
            cat_name={"cat_name": "KIDS"}
        elif re.search("(?i)398", i):
            cat_name={"cat_name": "IDEAS PRET"}
        yield scrapy.Request(i, callback=self.all_products, meta=cat_name)

    def all_products(self, response):
        product_urls=response.xpath('//*[@class="cdz-product-top"]/a/@href').extract()
        for url in product_urls:
            yield scrapy.Request(url, callback=self.product_page, meta=response.meta)
        next_page_url=response.xpath('//*[@title="Next"]/@href').extract_first()
        if next_page_url!=None:
            yield scrapy.Request(next_page_url, callback=self.all_products,  meta=response.meta)
    def product_page(self,response):
        image=response.xpath('//*[@class="MagicZoom"]/@href').extract_first()
        product_title=response.xpath('//*[@class="page-title"]/span/text()').extract_first()
        price=response.xpath('//*[@data-price-type="finalPrice"]/span/text()').extract_first()
        converted_price=0
        if price!=None:
            match= re.search(r'([\D]+)([\d,]+)',price)
            converted_price=int(match.group(2).replace(',',''))
        page_url=response.url
        yield {'img_url':image,
               'title':product_title,
               'Price':converted_price,
               'prod_page': page_url,
               'cat_name': response.meta['cat_name'],
               'Brand':'Gul Ahmed'
        }
