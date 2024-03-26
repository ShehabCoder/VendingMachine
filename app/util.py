from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import Depends
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import *
import logging

logging.basicConfig(level=logging.ERROR,format='----->%(asctime)s - %(name)s - %(message)s ') 

pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hashing(value):

    return  pwd.hash(value)

def verify(password, hashed_password):
    return pwd.verify(password, hashed_password)


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


params = {
    "host": DB_HOST,
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
}



def get_db_conn_cur()  :
    try:
        
        conn=psycopg2.connect(host=params["host"],
                            database=params["database"],
                            user=params["user"],
                            password=params["password"],
                            cursor_factory=RealDictCursor)
        logging.error("Connected to Database Successfully")
        return [conn,conn.cursor()]
    except Exception as e:
        logging.error(f'faild to connect with database {e}')
        time.sleep(2)



def create_tables(Dependcies):
    # SQL commands to create tables
    users_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        role VARCHAR,
        deposit INTEGER,
        username VARCHAR,
        password VARCHAR
    )
    """

    products_table_sql = """
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR,
        price INTEGER,
        inventory INTEGER,
        is_sale BOOLEAN,
        created_at TIMESTAMP,
        seller_id INTEGER
    )
    """

    # Execute SQL commands to create tables
    conn=Dependcies[0]
    cur=Dependcies[1]
    cur.execute(users_table_sql)
    cur.execute(products_table_sql)
    conn.commit()