from datetime import datetime, timedelta
from typing import Tuple
from jdcrawlers.tools import StaticWebCrawler
import json

LAST_CRAWLED_TIME_FILE = '/jobAnalyze/jdcrawlers/last_crawled_time_104.txt'
RAW_DATA_FILE = '/jobAnalyze/jdcrawlers/raw_data_104.txt'

class Crawler104(StaticWebCrawler):

    def __init__(self, keyword, sort='1', asc='1', filter_params=None) -> None:
        super().__init__()
        self.keyword = keyword
        self.sort = sort
        self.asc = asc
        self.filter_params = filter_params

    def crawl(self) -> Tuple[bool, str]:
        with open(LAST_CRAWLED_TIME_FILE, 'r') as f:
            last_crawled_time = f.read()
            last_crawled_time = datetime.strptime(last_crawled_time, "%Y-%m-%d %H:%M:%S")

        next_time_to_crawl = last_crawled_time + timedelta(seconds=10)
        if next_time_to_crawl > datetime.now():
            return False, f'Please try again after {next_time_to_crawl.strftime("%Y-%m-%d %H:%M:%S")}.'

        self.save_raw_data()

        with open(LAST_CRAWLED_TIME_FILE, 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return True, 'You can try to analyze 104 data now.'

    def save_raw_data(self) -> None:
        self.headers['Referer'] = 'https://www.104.com.tw/jobs/search/'
        url = 'https://www.104.com.tw/jobs/search/list'
        query = f'ro=0&kwop=7&keyword={self.keyword}&expansionType=area,spec,com,job,wf,wktm&mode=s&jobsource=2018indexpoc'
        if self.filter_params:
            query += ''.join([f'&{key}={value}' for key, value, in self.filter_params.items()])

        query += f'&order={self.sort}&asc={self.asc}&page=1'

        response = self.get_response(url, headers=self.headers, params=query)
        data = response.json()
        
        with open(RAW_DATA_FILE, 'w') as f:
            f.write(json.dumps(data))
