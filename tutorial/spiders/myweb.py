import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('/home/thole/Downloads/tutorial/')

import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy.loader import ItemLoader
from tutorial.items import SchoolInfo

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import re
import pandas as pd

Max_depth=3
filters_scheme=r'^(javascript|mailto|tel)'
filters_pages=r'.*?(facebook|twitter|linkedin|youtube|yahoo|Flickr|apple|google).*?'
filters_extension=r'(\.pdf|\.jpg|\.mp4|\.png|\.jpeg|\.icon|\.doc|\.docx|\.xls|\.xlsx|\.js)$'

regex_scheme=re.compile(filters_scheme,re.IGNORECASE)
regex_pages=re.compile(filters_pages,re.IGNORECASE)
regex_extension=re.compile(filters_extension,re.IGNORECASE)

class myspider(scrapy.Spider):
    name = "myweb"
    '''
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(deny=('facebook.com', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(deny=('twitter.com', ))),
    
      
    )
    '''
    #start_urls =['https://www.britishschool.nl/']

    def start_requests(self):
        '''
        with open("urls.txt", "rt") as f:
            urls = [url.strip() for url in f.readlines()]
        '''
        t=pd.read_excel("input/SIS_project.xlsx")
        urls=t["Link"].dropna().values
        '''
        urls = [
            'http://www.aisr.nl/',
            'https://riss.wolfert.nl/',
            'https://www.britishschool.nl/'
  
        ]
        '''
        for url in urls:
            request=scrapy.Request(url=url, callback=self.parse_web)

            request.meta['item'] = url
            yield request

            #yield scrapy.Request(url=url, meta={'item_info':url},callback=self.parse)

    def parse_web(self, response):
    
        title=response.xpath('//title/text()').re(r'(?i)student|parent|log in|sign in|SIS|SIMS|information|staff|sign up|powerschool|ISAM')
        if len(title)>0:
            l = ItemLoader(item=SchoolInfo(), response=response)
            l.add_css('title',"title::text")
            l.add_value('depth',response.meta['depth'])
            l.add_value('link',response.url)
            l.add_value('school',response.meta['item'])
            print "load item:", l.load_item()
            yield l.load_item()
        
      
        if response.meta['depth'] < Max_depth:              
            links = response.css('a::attr(href)').extract() # list of links
            if links is not None:
                for link in links:
                    next_page = response.urljoin(link)
                    if (regex_scheme.search(next_page) is None and regex_extension.search(next_page) is None and regex_pages.search(next_page) is None):
                        yield scrapy.Request(next_page, callback=self.parse_web,meta={'item':response.meta['item']})
        
