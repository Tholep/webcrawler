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
filters_pages=r'.*?(amazon|johnlewis|eclipse-creative|telegraph|theguardian|pinterest|facebook|twitter|linkedin|youtube|yahoo|Flickr|apple|google|vimeo|instagram|cie|ibo|BBC|news|newsletter|calendar|job).*?'
filters_extension=r'(\.pdf|\.jpg|\.mp4|\.png|\.jpeg|\.icon|\.doc|\.docx|\.xls|\.xlsx|\.js|\.bz2|rss|RSS)$'

regex_schemes=re.compile(filters_scheme,re.IGNORECASE)
regex_pages=re.compile(filters_pages,re.IGNORECASE)
regex_extensions=re.compile(filters_extension,re.IGNORECASE)

class myspider(scrapy.Spider):
    name = "myweb"

    def start_requests(self):
        #input school links
        t=pd.read_excel("input/SG_SIS.xlsx")
        urls=t["Link"].dropna().values

        # send request to each links
        for url in urls:
            request=scrapy.Request(url=url, callback=self.parse_web)
            request.meta['school'] = url
            request.meta['previous']=url
            yield request
    def parse_web(self, response):
        filter_title_exclude=r'(?i)Download|map|photo|Newsletter|Calendar|summary|music|policy|Mr|Mrs|news|blog|Curriculum|summer|jobs|contact|arts|report|english|club'
        filter_title=r'(?i)user|username|password|platform|connect|portal|admission|student|parent|parental|log in|login|sign in|signin|apply|enroll|SIS|SIMS|MIS|sign up|powerschool|ISAM|Engage|Veracross|myschoolportal|SchoolBase'
        filter_body=r'(?i)\buser\b|\busername\b|\bpassword\b|\bplatform\b|\bportal\b|\blog in\b|\blogin\b|\bsign in\b|\bsignin\b|\bSIS\b|\bSIMS\b|\bMIS\b|\bsign up\b|\bpowerschool\b|\bISAM\b|\bEngage\b|\bVeracross\b|\bmyschoolportal\b|\bSchoolBase\b'
        title=response.xpath('//title/text()').re(filter_title)
        title_exclude=response.xpath('//title/text()').re(filter_title_exclude)
        body=response.xpath('//body//text()').re(filter_body)

        if (len(title_exclude)==0) and (len(title)>0 or len(body)>0):
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
