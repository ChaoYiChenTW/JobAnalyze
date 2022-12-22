"""main
放置API的地方
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse

from jdcrawlers.web104 import (Crawler104, TagasSorter, TagsData, TagsFetcher,
                               Web104Data)

app = FastAPI()

origins = [
    "http://localhost:8000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)



@app.get('/{keyword}', response_class=PlainTextResponse)
def home(keyword: str):
    return f'kw is {keyword}'


@app.get('/104/{keyword}', response_class=JSONResponse)
def crawl_104(keyword: str):
    c = Crawler104(keyword)
    status = c.crawl()
    if not status[0]:
        return {'message': 'Failed', 'detail': status[1]}
    return {'message': 'Successed', 'detail': status[1]}


@app.get('/104//tags', response_class=JSONResponse)
def get_tags():
    all_tags = TagsData()
    for data in Web104Data():
        tags = TagsFetcher(data).tags
        all_tags.insert(tags)
    tags_data = all_tags.tags_data
    return TagasSorter(tags_data).sorted_tags


if __name__ == '__main__':
    all_tags = TagsData()
    for data in Web104Data():
        tags = TagsFetcher(data).tags
        all_tags.insert(tags)
    tags_data = all_tags.tags_data
    print(TagasSorter(tags_data).sorted_tags)
    