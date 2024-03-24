import logging
from fastapi import APIRouter,Depends,HTTPException,status
from app import schemas
from app.util import get_db_conn_cur,hashing,verify
from app.oauth2 import create_user_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import encode, decode, PyJWTError

# # pip install PyJWT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
SECRET_KEY = "secret123"

userLogin=APIRouter(tags=["Authentication"])




@userLogin.post('/login')
async def UserLogin(userdata:OAuth2PasswordRequestForm=Depends(), Dependencies:list= Depends(get_db_conn_cur)):

    conn=Dependencies[0]
    cur=Dependencies[1]
    try:
        cur.execute('SELECT * FROM users WHERE username=%s', (userdata.username,))
        conn.commit()
        user= dict(cur.fetchone())
        # logging.error(f"================{user['password']}")
        # logging.error(f"================{userdata.password}")
        correctedPassword=verify(userdata.password,user['password'])
        # logging.error(f"================{bool(correctedPassword)}")
        if not user or not  correctedPassword :
            raise HTTPException(status_code=404, detail="Incorrect username or password")
        token=create_user_token({"username:":user['username'],"role":user['role']})
        logging.error(f"User =={token}== Login Successful")
        return token
        
    except Exception as e:
        conn.rollback()
        logging.error("An error occurred while trying to login the user")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e)) 













# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# class User(BaseModel):
#     username: str
#     email: str 
#     is_seller: bool

# # authentication 
# class UserCreate(BaseModel):
#     username: str
#     password: str
#     email: str
#     is_seller: bool


# from datetime import datetime, timedelta

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = encode(to_encode, SECRET_KEY, algorithm="HS256")
#     return encoded_jwt

# user = authenticate_user(...)
# access_token = create_access_token(
#     data={"sub": user.username}
# )

# def verify_password(plain_password, hashed_password):
#     return bcrypt.verify(plain_password, hashed_password)

# def get_user(db: Session, username: str):
#     return db.query(User).filter(User.username == username).first()

# def authenticate_user(db: Session, username: str, password: str):
#     user = get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# @app.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Incorrect username or password")
#     # credentials check passes
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}

# # authorization
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, username=username)
#     if user is None:
#         raise credentials_exception
#     return user

# @app.get("/products/", response_model=List[Product])
# def read_products(current_user: User = Depends(get_current_user)):
#     if current_user.is_seller:
#         # seller can retrieve all products
#         return crud.get_products() 
#     else:
#         # buyer can only retrieve, not update
#         return crud.get_products()

