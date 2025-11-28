from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

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

class Item(BaseModel):
    title: str
    body: str
    published_status: Optional[bool]

@app.post("/blog")
def create_blog(item:Item):
    return item
    return {'data':f'Blog Created As {item.title}'}