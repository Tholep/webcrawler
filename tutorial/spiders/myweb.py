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
        urls = [
            'http://www.aisr.nl/',
            'https://riss.wolfert.nl/',
            'https://www.britishschool.nl/'
  
        ]
        
        for url in urls:
            request=scrapy.Request(url=url, callback=self.parse_web)

            request.meta['item'] = url
            yield request

            #yield scrapy.Request(url=url, meta={'item_info':url},callback=self.parse)

    def parse_web(self, response):
        #get content
        #only record titles with key words of interests
        print "*************************************"
        print "*************************************"
        print response.meta
        print "*************************************"
        print "*************************************"

        title=response.xpath('//title/text()').re(r'(?i)student|parent|log in|sign in|SIS|SIMS|information|staff|sign up|powerschool|ISAM')
        if len(title)>0:
            l = ItemLoader(item=SchoolInfo(), response=response)
            l.add_css('title',"title::text")
            l.add_value('depth',response.meta['depth'])
            l.add_value('link',response.url)
            l.add_value('school',response.meta['item'])
            print "load item:", l.load_item()
            yield l.load_item()
        
        '''
        yield { "title":response.css("title::text").extract(),
                       
                "depth":response.meta['depth'],
                #"previous":response.meta['download_slot'],
                "link":response.url,
        }
        '''
        #item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')

        #get next pages : list of link from href ( deny : ico, js,css, pdf,) , allow = html, 
        print "**********************************************************"
        #print "%s with depth of %s from %s - %s" % (response.url,response.meta['depth'],response.meta['download_slot'],response.meta['item'])
        print "**********************************************************"
        
        if response.meta['depth'] < 2:              
            links = response.css('a::attr(href)').extract() # list of links
            if links is not None:
                for link in links:
                    next_page = response.urljoin(link)
                    regex=r'(facebook|twitter|linked).*)'
                    if not re.search(regex,next_page):
                    
                        yield scrapy.Request(next_page, callback=self.parse_web,meta={'item':response.meta['item']})
        
