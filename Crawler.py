import os
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.item import Item, Field
from Graph import Graph

class PageDicItem(Item): # A data storage class(like directory) to store the extracted data
    url = Field()
    url_id = Field()

class Crawler(CrawlSpider):
    name = 'gcspider'
    #\allowed_domaines = ['www.grinnell.edu']
    #start_urls = ['https://www.grinnell.edu.html', 'https://en.wikipedia.org/wiki/Grinnell_College',
    # "https://www.cs.grinnell.edu"]

    start_urls = ['https://www.grinnell.edu.html']
    
    rules = (
        #Rule(
        #    LxmlLinkExtractor(allow='https://github.com/[\w-]+/[\w-]+$', allow_domains=['grinnell.edu', "en.wikipedia.org"]), 
        #    callback='parse_product_page', follow=True # this will continue crawling through the previously extracted links
        #)
        Rule(follow=True)
    )

    def __init__(self):
        self.dic_id = 0
        self.webGraph = Graph ()

    def parse(self, response):
        """
			A method to crawl a URL
		"""
        print("processing: " + response.url)

        # Store in URL dictionary
        self.dic_id = self.dic_id + 1
        item = PageDicItem ()
        item['url'] = response.url
        item['url_id'] = self.dic_id
        return item

        for webpage in response.css('.entry-title a ::attr("href")').extract():
            #yield response.follow(webpage, callback=self.store_content)
            webGraph.insert_edge()
            yield response.follow(webpage, callback=self.parse)
        
    
    def store_content (self, response):
        content = response.xpath(".//div[@class='entry-content']/descendant::text()").extract()
        f = open("Contents/{}.txt".format(response.url), "W+")
        f.write(content)
        f.close()