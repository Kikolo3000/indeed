from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

import scrapy
from indeed.items import IndeedItem

from bs4 import BeautifulSoup

class IndeedSpider(CrawlSpider):

#    name                    =   "indeed2"
#    allowed_domains         =   ["indeed.com", "indeed.co.uk", "de.indeed.com", "indeed.com.br", "indeed.es", "indeex.hk"]
#    #handle_httpstatus_list  =   [301, 302]
#    item_count = 0
#    start_urls = [
#        "https://www.indeed.com/jobs?q=e-learning"
#    ]
#
#    rules = (
#      # Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_search", follow = True),
#      Rule(LinkExtractor(allow=(), restrict_xpaths=("//a[contains(@href, 'start')]",))),
#      Rule(LinkExtractor(allow=(), restrict_xpaths=("//div[@class='title']",)), callback="parse_indeed_results", follow = True),
#    )
#
#    def parse_indeed_results(self, response):
#        
#        # To extract elements, add them here
#        xpaths = {
#            "title"       : "//h3/text()",
#            "company"     : "//div[contains(@class,'jobsearch-JobInfoHeader-subtitle')]",
#            "description" : "//div[contains(@id,'jobDescriptionText')]"
#            #"place"       : scrapy.Field(serializer=str)
#            #"salary"      : scrapy.Field(serializer=str)
#        }
#
#        item                 =   IndeedItem()
#        anyResultsExtracted  =   False
#
#        # Run xpath queries in sequence
#        for key, xpath_query in xpaths.items():
#            
#            # Run the xpath query against the target element
#            extracted = response.xpath(xpath_query).extract()
#            print(key, extracted)
#
#            # Make sure it found something
#            if len(extracted) > 0:
#
#                # Because there are nested elements represending the summary (multiple spans), we can use Beautfulsoup
#                # to pull out all everything as text without having to do complicated parsing methods or joining
#                if key == "company":
#                    soup      =  BeautifulSoup(extracted[0], 'html.parser')
#                    item[key] =  soup.get_text()
#                else:
#                    item[key] = extracted[0]
#
#                # We have to have at least one extracted item to qualify the row
#                anyResultsExtracted = True
#          
#        self.item_count += 1
#        if self.item_count > 10:
#            raise CloseSpider('item_exceeded')
        # If we have at least one item extracted per result, we put it into the model
        #print("\nitem no: ", self.item_count, "   title:", item["title"],"   company:", item["company"],"   description:", item["description"],"\n")
    name                    =   "indeed"
    allowed_domains         =   ["indeed.com"]
    #handle_httpstatus_list  =   [301, 302]
    item_count = 0
    #start_urls = [
    #    "https://www.indeed.com/jobs?q=e-learning"
    #]

    def __init__(self, *a, **kw) :
      self.PAGES  = None
      super(IndeedSpider, self).__init__(*a, **kw)
    
    def start_requests(self) :
      if not self.PAGES :
        raise CloseSpider("ERROR: <PAGES> is not defined [0-]")
      else :
        self.PAGES = int(self.PAGES)

      for page in range(0,self.PAGES) :
        URL="https://www.indeed.com/jobs?q=e-learning&start=%s"
        yield scrapy.Request(url = URL % str(page*10), callback = self.parse_urls )

    def parse_urls(self, response ) :
      JKs = response.xpath('//div[contains(@class,"jobsearch-SerpJobCard")]/@data-jk').extract()
      URL = "https://www.indeed.com/viewjob?jk=%s&from=web&vjs=3"
      for JK in JKs :
        yield scrapy.Request(url = URL % JK, callback = self.parse_indeed_results ) 

    def parse_indeed_results(self, response):
        self.log("PAPA")
        #LIMIT
        """
        self.item_count += 1
        if self.item_count > 10:
            raise CloseSpider('item_exceeded')
        """

        # To extract elements, add them here
        item  = IndeedItem()
       
        #TITLE
        title = response.xpath('//h3[contains(@class,"JobInfoHeader")]/text()').extract_first()
        item['title'] = title.strip()
        
        #COMPANY
        company_data = response.xpath('//div[contains(@class,"InlineCompanyRating")]//text()').extract()
        item['company'] = company_data[0].strip()
        item['address'] = company_data[-1].strip()
        
        #DESCRIPTION
        description = response.xpath('//div[contains(@id,"jobDescriptionText")]//text()').extract()
        description = ' '.join(description)
        item['description'] = description.replace("\n","").encode('utf-8')

        yield item
