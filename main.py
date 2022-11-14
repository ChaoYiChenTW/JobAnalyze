"""main
放置API的地方
"""
from ast import keyword
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from jdcrawlers.crawler104 import Crawler104

app = FastAPI()


@app.get('/{keyword}')
def home(keyword: str):
    return f'kw is {keyword}'


@app.get('/104/{keyword}')
def crawl_104(keyword: str):
    c = Crawler104(keyword)
    status = c.crawl()
    if not status[0]:
        return {'message': 'Failed', 'detail': status[1]}
    return {'message': 'Successed', 'detail': status[1]}

    