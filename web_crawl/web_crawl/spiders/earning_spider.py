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

        dividend_row = response.xpath("//td[contains(text(),'Dividend Per Share')]/ancestor::tr")
        dividend = [dividend_row.xpath('td[' + str(i) + ']/text()').extract_first() for i in range(2, 7)]

        dividend_payout_row = response.xpath("//td[contains(text(),'Dividend Payout')]/ancestor::tr")
        dividend_payout = [dividend_payout_row.xpath('td[' + str(i) + ']/text()').extract_first() for i in range(2, 7)]

        eps_growth_row = response.xpath("//td[contains(text(),'EPS Growth')]/ancestor::tr")
        eps_growth = [eps_growth_row.xpath('td[' + str(i) + ']/text()').extract_first() for i in range(2, 7)]

        earning_records = [
            EarningRecord(
                stock=request_stock_code,
                period=item[0],
                earning=item[1],
                dividend=item[2],
                dividend_payout=item[3],
                eps_growth=item[4]
            ) for item in zip(years, earnings, dividend, dividend_payout, eps_growth)]

        yield {
            'records': earning_records
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
