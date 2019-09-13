# -*- coding: utf-8 -*-
import scrapy
# from Graph import Graph


class CrawlwebSpidersSpider(scrapy.Spider):
    name = 'crawlWeb.spiders'
    allowed_domains = ['http://www.grinnell.edu']
    start_urls = ['http://http://www.grinnell.edu/']
    id = 0

     def parse(self, response):
        """
			A method to crawl a URL
		"""
        print("Processing: "+ response.url)

        # Get content from response

        
        # Append information at URL dictionary 
        yield {'id': id, 'url': response.url}
        id += 1

        # Build Web Graph
        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
        
        for next_page in response.css('a.next-posts-link'):
            ## Add to graph insert_edge
            yield response.follow(next_page, self.parse)
        
        