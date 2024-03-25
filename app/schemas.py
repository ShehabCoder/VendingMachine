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
    deposit:Optional[int]=0
    role:str

    @validator('role')
    def check_role(cls, role: str):
        if role not in ('seller', 'buyer'):
            raise ValueError("Invalid Role")
        return role
    
    @validator('deposit')
    def check_role(cls, deposit: str):
        if deposit not in (5,10,20,50,100):
            raise ValueError("Invalid Deposit Only Allowed (5,10,20,50,10)")
        return deposit
    

class deposit(BaseModel):
  
    deposit:int=0
    
    @validator('deposit')
    def check_role(cls, deposit: str):
        if deposit not in (5,10,20,50,100):
            raise ValueError("Invalid Deposit Only Allowed (5,10,20,50,10)")
        return deposit
    

class userDelete(BaseModel):
    id:int 


class userLogin(BaseModel):
    username:str
    password:str
    
