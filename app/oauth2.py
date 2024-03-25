from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
def create_user_token(data:dict):

    to_encode=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update( {"exp": expire} )

    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return { 'access_token': f'{token}','token_type':'bearer'}


def get_current_user(token:dict=Depends(oauth2_scheme)):

    try:
        logging.error("Toketn=======> %s is",token)
        # token=token['access_token']
        payload=jwt.decode(token,SECRET_KEY,ALGORITHM)
        # payload=jwt.decode(payload,SECRET_KEY,ALGORITHM)
        logging.error("Payload=======> %s is",payload)
        username=payload['username']
        logging.error("User %s tried to authenticate",username)
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials",headers={"WWW-Authriazation"})
        return payload   
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"--------------get_current_usermethod{str(e)}")
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials")
    

