# from fastapi import Body
from app import schemas
from fastapi import FastAPI,Response,status,HTTPException,APIRouter,Depends
import psycopg2
from typing import Annotated
from app.util import hashing,get_db_conn_cur,create_tables
from app.routers.products import productRouter 
from app.routers.purchase import purchaseRouter 
from app.routers.users import userRouter 
from app.routers.auth import userLogin 
from psycopg2.extensions import connection,cursor
import psycopg2


Dependcies=get_db_conn_cur()
create_tables(Dependcies)






app=FastAPI()
app.include_router(productRouter)
app.include_router(userRouter)
app.include_router(userLogin)
app.include_router(purchaseRouter)


