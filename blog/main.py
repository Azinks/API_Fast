from fastapi import FastAPI,Depends,Response,HTTPException,status
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .hashing import hash_password

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
    """ "synchronize_session=False means:" Dont try to update ORM objects in the session — we don’t need it, just execute the SQL delete fast """
    deleted=db.query(models.Blog).filter(models.Blog.id==id)
    prev_id=id
    if not deleted.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Not Found {id}')
    else:
        deleted.delete(synchronize_session=False)
        db.commit()
    return {'Done':prev_id}

@app.get('/blog',status_code=status.HTTP_302_FOUND,response_model=List[schemas.ResponseBlog])
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

@app.put('/blog/{id}')
def blog_update(id:int,request:schemas.Blog,db:Session=Depends(get_db)):
    updated = db.query(models.Blog).filter(models.Blog.id==id)
    blog=updated.first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog Not Found {id}')
    else:
        updated.update({models.Blog.title:'Start_Updating'},synchronize_session=False)
        db.commit()
    db.refresh(blog)#{"details": "updated", "id": id}   
    return blog

@app.post('/user',response_model=schemas.ResponseUser)
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    hashPass = hash_password(request.password)
    new_user = models.User(id=request.id,user_name=request.username,email=request.email,password=hashPass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user',status_code=status.HTTP_200_OK ,response_model=List[schemas.ResponseUser])
def fetch_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.delete('/user/{id}')
def delete_user(id:int,db:Session=Depends(get_db)):
    deleted=db.query(models.User).filter(models.User.id==id)
    prev_id=id
    if not deleted.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Not Found {id}')
    else:
        deleted.delete(synchronize_session=False)
        db.commit()
    return {'Done':prev_id}

@app.put('/user/{id}')
def update_user(id:int,new_id:int,request:schemas.User,db:Session=Depends(get_db)):
    updated = db.query(models.User).filter(models.User.id==id)
    prev_id = updated.first()
    if not prev_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User Not Found {id}')
    else:
        updated.update({models.User.id:new_id},synchronize_session=False)
        db.commit()
    return f'Sucess' 