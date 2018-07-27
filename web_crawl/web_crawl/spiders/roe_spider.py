import scrapy
from scrapy.http.request import Request
import re

from web_crawl.items import RoeRecord


class RoeSpider(scrapy.Spider):
    name = 'roe'

    custom_settings = {
        'ITEM_PIPELINES': {
            'web_crawl.pipelines.RoeMongoPipeline': 400
        }
    }

    def parse(self, response):
        request_stock_code = self.extract_request_stock_code(response)

        roe_row = response.xpath("//td[contains(text(),'Return on Equity')]/ancestor::tr")
        roes = [roe_row.xpath('td[' + str(i) + ']/text()').extract_first() for i in range(2, 7)]

        year_row = response.xpath("//td[contains(text(),'Closing Date')]/ancestor::tr")
        years = [year_row.xpath('td[' + str(i) + ']/text()').extract_first() for i in range(2, 7)]

        roe_records = [
            RoeRecord(
                stock=request_stock_code,
                period=item[0],
                roe=item[1]) for item in zip(years, roes)]

        yield {
            'records': roe_records
        }

    def start_requests(self):
        with open("stock_input.csv") as f:
            lines = f.readlines()
        stock_codes = [line.replace('\n', '').replace(u'\ufeff', '') for line in lines]
        for stock_code in stock_codes:
            url = f"http://www.aastocks.com/en/stocks/analysis/company-fundamental/financial-ratios?symbol={stock_code}"
            yield Request(url, self.parse)

    @staticmethod
    def extract_request_stock_code(response):
        request_url = response.request.url
        pattern = re.compile(r"symbol=([0-9]*)")
        return pattern.search(request_url)[1]
