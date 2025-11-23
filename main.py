from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": {'world','new'}}

@app.get('/blog')
def show(limit,published:bool,sort:Optional[str]=None):

    if published:
        return{'data':f'{limit} has been published'}
    else:
        return{'data':f'{limit} has not been published'}


@app.get("/blog/{id}/comments")
def num(id:int,limit=10):

    return{'data':id}

@app.get('/about')
def about():
    return {"About" :{"About Page"}}
