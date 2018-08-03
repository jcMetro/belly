import scrapy
from scrapy.http.request import Request
import re

from web_crawl.items import EarningRecord


class EarningSpider(scrapy.Spider):
    name = 'earning'

    custom_settings = {
        'ITEM_PIPELINES': {
            'web_crawl.pipelines.EarningMongoPipeline': 400
        }
    }

    def parse(self, response):
        request_stock_code = self.extract_request_stock_code(response)

        earning_row = response.xpath("//td[contains(text(),'Earnings Per Share')]/ancestor::tr")
        earnings = [earning_row.xpath('td[' + str(i) + ']/text()').extract_first() for i in range(2, 7)]

        year_row = response.xpath("//td[contains(text(),'Closing Date')]/ancestor::tr")
        years = [year_row.xpath('td[' + str(i) + ']/text()').extract_first() for i in range(2, 7)]

        roe_records = [
            EarningRecord(
                stock=request_stock_code,
                period=item[0],
                earning=item[1]) for item in zip(years, earnings)]

        yield {
            'records': roe_records
        }

    def start_requests(self):
        with open("stock_input.csv") as f:
            lines = f.readlines()
        stock_codes = [line.replace('\n', '').replace(u'\ufeff', '') for line in lines]
        for stock_code in stock_codes:
            url = f"http://www.aastocks.com/en/stocks/analysis/company-fundamental/earnings-summary?symbol={stock_code}"
            yield Request(url, self.parse)

    @staticmethod
    def extract_request_stock_code(response):
        request_url = response.request.url
        pattern = re.compile(r"symbol=([0-9]*)")
        return pattern.search(request_url)[1]
