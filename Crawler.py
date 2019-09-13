import scrapy
#from Graph import Graph

class Crawler(scrapy.Spider):
    name = 'gcspider'
    #allowed_domaines = ['www.grinnell.edu']
    start_urls = ['https://www.grinnell.edu.html']

    def parse(self, response):
        """
			A method to crawl a URL
		"""
        print("processing: "+response.url)
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::test').get()}
        
        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse)
