from pydantic import BaseModel

"""IT DEPICTS ABOUT THE INPUT ON (POST) METHOD"""

class Blog(BaseModel):
    id :int
    title: str
    body : str