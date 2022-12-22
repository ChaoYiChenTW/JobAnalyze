import json
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Tuple

import jieba.analyse

from jdcrawlers.tools import StaticWebCrawler

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



class Web104Data:

    def __init__(self) -> None:
        self.path = RAW_DATA_FILE

    def __iter__(self):
        with open(self.path) as f:
            all_data = json.loads(f.read())
            for job in all_data['data']['list']:
                yield job


class TagsData:
    
    def __init__(self) -> None:
        self._tags_data = defaultdict(self._zero)

    def insert(self, tags: list) -> None:
        for tag in tags:
            self._tags_data[tag[0]] += tag[1]

    @property
    def tags_data(self) -> dict:
        return self._tags_data

    @staticmethod
    def _zero():
        return 0


class TagsFetcher:

    def __init__(self, data: dict) -> None:
        self.data = data
        self._tags = jieba.analyse.extract_tags(self.data['description'], topK=50, withWeight=True)

    @property
    def tags(self) -> list:
        return self._tags

class TagasSorter:

    def __init__(self, tags_data: defaultdict) -> None:
        self.tags_data = tags_data
        self._sorted_tags = self._sort_tags()

    def _sort_tags(self) -> list:
        return [{'Text': k, 'Value': v} for k, v in sorted(self.tags_data.items(), key=lambda item: item[1], reverse=True)]

    @property
    def sorted_tags(self) -> list:
        return self._sorted_tags

if __name__ == '__main__':
    all_tags = TagsData()
    for data in Web104Data():
        tags = TagsFetcher(data).tags
        all_tags.insert(tags)
    tags_data = all_tags.tags_data
    print(TagasSorter(tags_data).sorted_tags)

    