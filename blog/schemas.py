from pydantic import BaseModel

"""IT DEPICTS ABOUT THE INPUT ON (POST) METHOD"""

class Blog(BaseModel):
    id : int
    title: str
    body : str

class ResponseBlog(BaseModel):
    id : int
    title : str
    class Config():
        orm_mode = True

class User(BaseModel):
    id :int
    username : str
    email : str
    password : str

class ResponseUser(BaseModel):
    id : int
    user_name : str

    class Config():
        orm_mode = True
            
