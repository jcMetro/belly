import scrapy
from scrapy.http.request import Request
import re

class BlogSpider(scrapy.Spider):
    name = 'stocks'

    def parse(self, response):
        rows = response.xpath("//div[contains(@class, 'title') and text()='Dividend History']/ancestor::div[2]//table//tr")
        request_url = response.request.url
        pattern = re.compile(r"symbol=([0-9]*)")
        request_stock_code = pattern.search(request_url)[1]
        for row in rows[1:]: 
            yield {
                'stock' : request_stock_code,
                'period': row.xpath("td[2]/text()").extract_first(),
                'dividend': row.xpath("td[4]/text()").extract_first()
            }

    def start_requests(self):
        with open("stock_input.csv") as f:
            content = f.readlines()
        stockCodes = [line.split(",")[1].replace(r'"', '') for line in content[1:]]
        for stockCode in stockCodes:
            url = f"http://www.aastocks.com/en/stocks/analysis/company-fundamental/dividend-history?symbol={stockCode}&filter=D"
            yield Request(url, self.parse)

