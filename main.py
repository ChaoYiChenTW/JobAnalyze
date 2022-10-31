from ast import keyword
from fastapi import FastAPI

app = FastAPI()


@app.get('/{keyword}')
def home():
    return f'kw is {keyword}'