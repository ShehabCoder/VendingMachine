# # pip install PyJWT
# # SECRET_KEY = "secret123"
# # from jwt import encode, decode, PyJWTError


# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


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

