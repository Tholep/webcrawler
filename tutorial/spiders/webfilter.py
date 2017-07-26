import scrapy


class myspider(scrapy.Spider):
    name = "webfilter"
    def start_requests(self):
        '''
        with open("urls.txt", "rt") as f:
            urls = [url.strip() for url in f.readlines()]
        '''
        urls = [
            #'http://www.aisr.nl/',
            #'https://riss.wolfert.nl/',
            'https://www.britishschool.nl/'
  
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    '''
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
    '''
    def parse(self, response):
        #get content
        #only record titles with key words of interests
        title=response.xpath('//title/text()').re(r'(?i)student|parent|log in|sign in|SIS|SIMS|system|information|administrator|admin|staff')
        if len(title)>0:
            yield { "title":response.css("title::text").extract(),
                           
                    "depth":response.meta['depth'],
                    #"previous":response.meta['download_slot'],
                    "link":response.url,
            }
            #item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')

        #get next pages : list of link from href ( deny : ico, js,css, pdf,) , allow = html, 
        print "**********************************************************"
        print "%s with depth of %s from %s" % (response.url,response.meta['depth'],response.meta['download_slot'])
        print "**********************************************************"
        if response.meta['depth'] < 3:  
            
            links = response.css('a::attr(href)').extract() # list of links
            if links is not None:
                for link in links:
                    next_page = response.urljoin(link)
                
                    yield scrapy.Request(next_page, callback=self.parse)

if __name__ == '__main__':
    import scrapy
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    process = CrawlerProcess(get_project_settings())

    # 'followall' is the name of one of the spiders of the project.
    process.crawl("myweb")
    process.start() # the script will block here until the crawling is finished