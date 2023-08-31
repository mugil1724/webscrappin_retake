import scrapy
from scrapy.http import Request  # Add this line to import Request
from scrapy.selector import Selector
from scrapy.http import FormRequest
import re
from urllib.parse import urlparse
import pandas as pd

class RunningSpider(scrapy.Spider):
    name = "drama"
    
    custom_settings = {
        'FEEDS': {
            'items.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'overwrite': True,
                #'fields': ['field1', 'field2', 'field3'],  # Add your desired fields here
            },
        },
    }
   
    def start_requests(self):
        self.items_processed = 0  # Initialize the counter
        self.item_limit = 101     # Set the maximum number of items to process
        

        start_urls=['https://mydramalist.com/people/top']

     
        for url in start_urls:
            headers = {
                'authority': 'mydramalist.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://mydramalist.com/people/top',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }
            
    

            yield scrapy.Request(url=url,callback=self.get_list,headers=headers)


    def get_list(self,response):


        headers = {
            'authority': 'mydramalist.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://mydramalist.com/people/top',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        links=response.xpath('//h6/a/@href').extract()
        
        for link in links:
            link="https://mydramalist.com"+link
            print(link)
            
            yield scrapy.Request(url=link,callback=self.get_category,headers=headers)

        np=response.xpath('//li[@class="page-item next"]/a/@href').get()
        if np:
            np="https://mydramalist.com"+np
            yield scrapy.Request(url=np,callback=self.get_list,headers=headers)


    def get_category(self,response):

        name=response.xpath('//h1[@class="film-title m-b-0 m-r-0"]/text()').get()
        item={}
        item['name']=name
        i=0
        td_elements = response.xpath('//table[@class="table film-list"]//tr').getall()

        data = Selector(text=td_elements[1])
        td_elements = data.xpath('.//td//text()').getall()
        for data in td_elements:
            i=str(i)
            data=data.split('\n')[0]
            if data:
                # print(data)
                
                item[i]=data
                i=int(i)
                i=i+1
        if self.items_processed >= self.item_limit:
            self.crawler.engine.close_spider(self, 'Reached item limit')

        self.items_processed += 1
        yield item

    def close_spider(self, reason):
        pass
