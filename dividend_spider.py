import scrapy

class BlogSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['http://www.aastocks.com/en/stocks/analysis/company-fundamental/dividend-history?symbol=01052&filter=D']

    def parse(self, response):
        rows = response.xpath("//div[contains(@class, 'title') and text()='Dividend History']/ancestor::div[2]//table//tr")
        for row in rows[1:]: 
            yield {
                'period': row.xpath("td[2]/text()").extract_first(),
                'dividend': row.xpath("td[4]/text()").extract_first()
            }


