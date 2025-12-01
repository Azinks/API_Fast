from fastapi import FastAPI,Depends
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:

        yield db #yield is basically does not stop the function on execution like return fuction ,Lets API have limited Results
                 
    finally:

        db.close()    

@app.post('/blog',status_code=201)
def create(request:schemas.Blog,db:Session=Depends(get_db)): 
    """coverting "Session" Into Pydantic model By "Depends"""
    new_blog = models.Blog(id=request.id,title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all_items(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def display_id(id:int,db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id==id).first()
    return blogs