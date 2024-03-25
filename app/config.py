# # pip install PyJWT
# # SECRET_KEY = "secret123"
# # from jwt import encode, decode, PyJWTError


# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# from datetime import datetime, timedelta







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

