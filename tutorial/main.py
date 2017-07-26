import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy.loader import ItemLoader
from items import SchoolInfo
from spiders.myweb import myspider
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':


    
    process = CrawlerProcess(get_project_settings())
    #with open(url,w) as f:
    #   f.write(url)

    # 'followall' is the name of one of the spiders of the project.
    process.crawl("myweb")
    process.start() # the script will block here until the crawling is finished