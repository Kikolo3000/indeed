from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

import scrapy
from indeed.items import IndeedItem

from bs4 import BeautifulSoup

class IndeedSpider(CrawlSpider):

    name                    =   "indeed2"
    allowed_domains         =   ["indeed.com", "indeed.co.uk", "de.indeed.com", "indeed.com.br", "indeed.es", "indeex.hk"]
    handle_httpstatus_list  =   [301, 302]
    item_count = 0
    start_urls = [
        "https://www.indeed.com/jobs?q=e-learning"
    ]

    rules = (
      # Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_search", follow = True),
      Rule(LinkExtractor(allow=(), restrict_xpaths=("//a[contains(@href, 'start')]",))),
      Rule(LinkExtractor(allow=(), restrict_xpaths=("//div[@class='title']",)), callback="parse_indeed_results", follow = True),
    )

    def parse_indeed_results(self, response):
        
        # To extract elements, add them here
        xpaths = {
            "title"       : "//h3/text()",
            "company"     : "//div[contains(@class,'jobsearch-JobInfoHeader-subtitle')]",
            "description" : "//div[contains(@id,'jobDescriptionText')]"
            #"place"       : scrapy.Field(serializer=str)
            #"salary"      : scrapy.Field(serializer=str)
        }

        item                 =   IndeedItem()
        anyResultsExtracted  =   False

        # Run xpath queries in sequence
        for key, xpath_query in xpaths.items():
            
            # Run the xpath query against the target element
            extracted = response.xpath(xpath_query).extract()
            print(key, extracted)

            # Make sure it found something
            if len(extracted) > 0:

                # Because there are nested elements represending the summary (multiple spans), we can use Beautfulsoup
                # to pull out all everything as text without having to do complicated parsing methods or joining
                if key == "company":
                    soup      =  BeautifulSoup(extracted[0], 'html.parser')
                    item[key] =  soup.get_text()
                else:
                    item[key] = extracted[0]

                # We have to have at least one extracted item to qualify the row
                anyResultsExtracted = True
          
        self.item_count += 1
        if self.item_count > 10:
            raise CloseSpider('item_exceeded')
        # If we have at least one item extracted per result, we put it into the model
        #print("\nitem no: ", self.item_count, "   title:", item["title"],"   company:", item["company"],"   description:", item["description"],"\n")
        yield item
