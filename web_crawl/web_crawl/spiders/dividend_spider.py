import scrapy
from scrapy.http.request import Request
import re

from web_crawl.items import DividendRecord

class DividendSpider(scrapy.Spider):
    name = 'dividend'

    def parse(self, response):
        request_stock_code = self.extract_request_stock_code(response)
        rows = response.xpath("//div[contains(@class, 'title') and text()='Dividend History']/ancestor::div[2]//table//tr")
        div_records = [DividendRecord(stock=request_stock_code, period=row.xpath("td[2]/text()").extract_first(), dividend=row.xpath("td[4]/text()").extract_first()) for row in rows[1:]]
        yield {
            'records' : div_records
        }

    def start_requests(self):
        with open("stock_input.csv") as f:
            content = f.readlines()
        stockCodes = [line.split(",")[1].replace(r'"', '') for line in content[1:]]
        for stockCode in stockCodes:
            url = f"http://www.aastocks.com/en/stocks/analysis/company-fundamental/dividend-history?symbol={stockCode}&filter=D"
            yield Request(url, self.parse)

    def extract_request_stock_code(self, response): 
        request_url = response.request.url
        pattern = re.compile(r"symbol=([0-9]*)")
        return pattern.search(request_url)[1]