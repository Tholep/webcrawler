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

Max_depth=2
filters_scheme=r'^(javascript|mailto|tel)'
filters_pages=r'.*?(facebook|twitter|linkedin|youtube|yahoo|Flickr|apple|google|vimeo).*?'
filters_extension=r'(\.pdf|\.jpg|\.mp4|\.png|\.jpeg|\.icon|\.doc|\.docx|\.xls|\.xlsx|\.js|\.bz2)$'

regex_schemes=re.compile(filters_scheme,re.IGNORECASE)
regex_pages=re.compile(filters_pages,re.IGNORECASE)
regex_extensions=re.compile(filters_extension,re.IGNORECASE)

class myspider(scrapy.Spider):
    name = "specific"

    def start_requests(self):
        #input school links
        t=pd.read_excel("input/UK_schools.xlsx")
        urls=t["Link"].dropna().values
        # send request to each link
        for url in urls:
            request=scrapy.Request(url=url, callback=self.parse_web)

            request.meta['school'] = url
            request.meta['previous']=url
            yield request
    def parse_web(self, response):
    
        title=response.xpath('//title/text()').re(r'(?i)portal|admission|student|parent|log in|login|sign in|signin|apply|enrol|SIS|SIMS|information|staff|sign up|powerschool|ISAM')
        if len(title)>0:
            l = ItemLoader(item=SchoolInfo(), response=response)
            l.add_css('title',"title::text")
            l.add_value('depth',response.meta['depth'])
            l.add_value('link',response.url)
            l.add_value('school',response.meta['school'])
            l.add_value('previous',response.meta['previous'])
            print "load item:", l.load_item()
            yield l.load_item()
        
      
        if response.meta['depth'] < Max_depth:              
            links = response.css('a::attr(href)').extract() # list of links
            if links is not None:
                for link in links:
                    next_page = response.urljoin(link)
                    if (regex_schemes.search(next_page) is None) and (regex_extensions.search(next_page) is None) and (regex_pages.search(next_page) is None):
                        yield scrapy.Request(next_page, callback=self.parse_web,meta={'school':response.meta['school'],'previous':response.url})
        
