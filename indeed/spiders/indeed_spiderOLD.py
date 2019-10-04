# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from indeed.items import *

import  json
import  unicodedata
import  os

#class IndeedSpider(scrapy.Spider):
class IndeedSpider(CrawlSpider):
  name = 'indeed'
  item_count = 0
  allowed_domain = ['https://www.indeed.es/', 'https://www.indeed.com/']
  start_urls = ['https://www.indeed.com/jobs?q=e-learning']
  #handle_httpstatus_list = [302]

  def parse(self, response):
    print('000000')
    items = []
    listOfResults = response.xpath('//div[contains(@class, "jobsearch-SerpJobCard")]//div[contains(@class, "title")]')
    print(len(listOfResults))

    for result in listOfResults:      
      item = IndeedItem()
      item['title'] = result.xpath('//h3/text()').extract_first()
      item['company'] = result.xpath('//div[contains(@class,"jobsearch-InlineCompanyRating")]//div[1]/a/text()').extract()
      #item['company'] = result.xpath('//div[contains(@class,"jobsearch-JobInfoHeader")]//div[1]//div[1]/text()').extract()

      #item['company'] = response.xpath('//div[contains(@class,"jobsearch-JobInfoHeader-subtitle")]//div[contains(@class,"icl-u-lg-mr--sm")][1]//text()').extract()
      item['place'] = result.xpath('//div[contains(@class,"jobsearch-JobInfoHeader")]//div[1]//div[last()]/text()').extract()
      item['salary'] = result.xpath('//div[contains(@class,"jobsearch-JobMetadataHeader-item")]//text()').extract()
      item['description'] = result.xpath('//div[contains(@class,"jobDescriptionText")]//text()').extract()
      items.append(item)
      print(item)
      self.item_count += 1
      if self.item_count > 10:
        raise CloseSpider('item_exceeded')
    return items
#  rules = {
#    # Para cada item
#    Rule(LinkExtractor(allow = (), restrict_xpaths = ('//div[contains(@class, "pagination")]/a[last()]//a'))),
#    Rule(LinkExtractor(allow =(), restrict_xpaths = ('//div[contains(@class, "jobsearch-SerpJobCard")]//*[contains(@class, "title")]//*[contains(@class, "  title")]')), callback = 'parse_item', follow = False)
#    }

#  def parse_item(self, response):        
#    item = IndeedItem()
#    #item = ItemLoader(item=IndeedItem(), response=response)
#    #info de producto
#    print ('\n\n element number %i in process \n \n' % self.item_count)
#    item['title'] = response.xpath('//h3/text()').extract_first()
#    item['company'] = response.xpath('//div[contains(@class,"jobsearch-JobInfoHeader")]//div[1]//div[1]/text()').extract()
#    #item['company'] = response.xpath('//div[contains(@class,"jobsearch-JobInfoHeader-subtitle")]//div[contains(@class,"icl-u-lg-mr--sm")][1]//text()').extract()
#    item['place'] = response.xpath('//div[contains(@class,"jobsearch-JobInfoHeader")]//div[1]//div[last()]/text()').extract()
#    item['salary'] = response.xpath('//div[contains(@class,"jobsearch-JobMetadataHeader-item")]//text()').extract()
#    item['description'] = response.xpath('//div[contains(@class,"jobDescriptionText")]//text()').extract()
#    self.item_count += 1
#    if self.item_count > 10:
#      raise CloseSpider('item_exceeded')
#    print ('\n element number %i done \n' % self.item_count)
#    yield item
