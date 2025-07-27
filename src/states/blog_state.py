from typing import TypedDict
from pydantic import BaseModel, Field

class Blog(BaseModel):
    title:str=Field(description="The Title of the Blog")
    content:str=Field(description="The Content of the Blog")

class BlogState(TypedDict):
    topic:str
    blog:Blog
    curr_lang:str