from fastapi import FastAPI,Depends,Response,HTTPException,status
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

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db:Session=Depends(get_db)): 
    """ Coverting "Session" Into Pydantic Model By "Depends" """
    new_blog = models.Blog(id=request.id,title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}')
def deleted_id(id:int,db:Session=Depends(get_db)):
    """ "synchronize_session=False means:" Don’t try to update ORM objects in the session — we don’t need it, just execute the SQL delete fast """
    deleted=db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Not Found {id}')
    else:
        db.commit()
    return {'Done':'Deleted {id}'}

@app.get('/blog',status_code=status.HTTP_302_FOUND)
def all_items(db:Session=Depends(get_db)):
    """Getting All The Values Stored Inside The DB"""
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK)
def display_id(id:int,response:Response,db:Session=Depends(get_db)):
    """ Getting A Single Value By {id} """
    blogs = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Item {id} Not Found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'details':f'Item {id} Not Found'}
    else:
        return blogs