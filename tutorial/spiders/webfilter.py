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
filters_extension=r'(\.pdf|\.jpg|\.mp4|\.png|\.jpeg|\.icon|\.doc|\.docx|\.xls|\.xlsx|\.js|\.bz2|rss|RSS)$'

regex_schemes=re.compile(filters_scheme,re.IGNORECASE)
regex_pages=re.compile(filters_pages,re.IGNORECASE)
regex_extensions=re.compile(filters_extension,re.IGNORECASE)

class myspider(scrapy.Spider):
    name = "webfilter"

    def start_requests(self):
        #input school links
      
        urls=["http://www.marymountlondon.com"]
        # send request to each link
        for url in urls:
            request=scrapy.Request(url=url, callback=self.parse_web)

            request.meta['school'] = url
            request.meta['previous']=url
            yield request
    def parse_web(self, response):
        filter_title=r'(?i)user|username|password|platform|connect|portal|admission|student|parent|log in|login|sign in|signin|apply|enrol|SIS|SIMS|information|staff|sign up|powerschool|ISAM|Engage|CapitaSIMS'
        filter_body=r'(?i)\buser\b|\busername\b|\bpassword\b|\bplatform\b|\bportal\b|\blog in\b|\blogin\b|\bsign in\b|\bsignin\b|\bSIS\b|\bSIMS\b|\bsign up\b|\bpowerschool\b|\bISAM\b|\bEngage\b|CapitaSIMS'
        title=response.xpath('//title/text()').re(filter_title)
        body=response.xpath('//body//text()').re(filter_body)
        if len(title)>0 or len(body)>0:
            l = ItemLoader(item=SchoolInfo(), response=response)
            l.add_css('title',"title::text")
            l.add_value('depth',response.meta['depth'])
            l.add_value('link',response.url)
            l.add_value('school',response.meta['school'])
            l.add_value('previous',response.meta['previous'])
            l.add_value('keywords',"_".join(set(body)))
            print "load item:", l.load_item()
            yield l.load_item()
        
      
        if response.meta['depth'] < Max_depth:              
            links = response.css('a::attr(href)').extract() # list of links
            if links is not None:
                for link in links:
                    next_page = response.urljoin(link)
                    if (regex_schemes.search(next_page) is None) and (regex_extensions.search(next_page) is None) and (regex_pages.search(next_page) is None):
                        yield scrapy.Request(next_page, callback=self.parse_web,meta={'school':response.meta['school'],'previous':response.url})
        
