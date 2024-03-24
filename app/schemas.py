from typing import Optional
from pydantic import BaseModel,validator


class productCreate(BaseModel):
    name:str
    price:int
    inventory:int
   
class productUpdate(BaseModel):
    name:Optional[str]
    price :Optional[int]
    inventory:Optional[int]
    

class user(BaseModel):
    username:str
    password:str
    # deposit:Optional[float]=0.0
    role:str

    @validator('role')
    def check_role(cls, role: str):
        if role not in ('seller', 'buyer'):
            raise ValueError("Invalid Role")
        return role
    
class userDelete(BaseModel):
    id:int 


class userLogin(BaseModel):
    username:str
    password:str
    
