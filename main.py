# from fastapi import Body
from app import schemas
from fastapi import FastAPI,Response,status,HTTPException,APIRouter,Depends
import psycopg2
from typing import Annotated
from app.util import hashing,get_db_conn_cur
from app.routers.products import productRouter 
from app.routers.purchase import purchaseRouter 
from app.routers.users import userRouter 
from app.routers.auth import userLogin 
from psycopg2.extensions import connection,cursor
# import logging
# from .app.routers.products  import router 


# logging.basicConfig(level=logging.ERROR,format='----->%(asctime)s - %(name)s - %(message)s ') 

# while True:
#     try:
#         conn=psycopg2.connect(host=params["host"],
#                               database=params["database"],
#                               user=params["user"],
#                               password=params["password"],
#                               cursor_factory=RealDictCursor)
#         cur=conn.cursor()
#         logging.error("Connected to Database Successfully")
#         # cur.execute(f"select * from products")
#         break
#     except Exception as e:
#         logging.error(f'faild to connect with database {e}')
#         time.sleep(2)

# def get_db_conn_cur()  :
#     try:
        
#         conn=psycopg2.connect(host=params["host"],
#                             database=params["database"],
#                             user=params["user"],
#                             password=params["password"],
#                             cursor_factory=RealDictCursor)
#         logging.error("Connected to Database Successfully")
#         return [conn,conn.cursor()]
#     except Exception as e:
#         logging.error(f'faild to connect with database {e}')
#         time.sleep(2)



app=FastAPI()
app.include_router(productRouter)
app.include_router(userRouter)
app.include_router(userLogin)
app.include_router(purchaseRouter)


# @app.get("/products")
# async def read_root(Dependcies:tuple=Depends(get_db_conn_cur)):
#     try:
#         conn=Dependcies[0]
#         cur=Dependcies[1]
#         cur.execute("""SELECT * FROM products """)
#         products=cur.fetchall()
#         conn.commit()
#         logging.debug("Products Fetched Succesfully")

#         return {"message": products }

#     except Exception as e:
#         logging.error("Faild To Fetch Data  From DB",exc_info=True)
#         conn.rollback()
#         return {"Error":str(e)}



# @app.post("/product",status_code=status.HTTP_201_CREATED)
# def create_a_product(product:schemas.productCreate,response:Response,Dependcies:tuple=Depends(get_db_conn_cur)):
#     """This is a POST request to create a new  product."""
#     # logging.error(f'Data rom user:Payload received {product.model_dump_json()}-{response.status_code}')
#     try:
#         conn=Dependcies[0]
#         cur=Dependcies[1]
#         cur.execute("""INSERT INTO products (name, price, inventory) VALUES (%s, %s, %s) RETURNING name , price,inventory;""",
#                    (product.name, product.price, product.inventory))
#         product=cur.fetchone()
#         conn.commit()
#         logging.error(f'Data received  From DataBase: {product}-{response.status_code}')
        
#         return {'Message': product}
#     except Exception as e :
#         logging.debug(f"Error in creating the data into table {e}")
#         response.status_code=status.HTTP_406_NOT_ACCEPTABLE
#         conn.rollback()
#         return { "Error": str(e)}
    
    

# @app.put("/product/{id}", status_code=status.HTTP_202_ACCEPTED)
# async def update_product(id: int, product: schemas.productUpdate, response: Response,Dependcies:tuple=Depends(get_db_conn_cur)):
#     try:
#         # Execute the SQL query to update the product
#         conn=Dependcies[0]
#         cur=Dependcies[1]
#         cur.execute("""UPDATE products 
#                         SET name = %s, price = %s, inventory = %s
#                         WHERE id = %s 
#                         RETURNING *;""",
#                     (product.name, product.price, product.inventory, id))
#         updated_product = cur.fetchone()

#         if updated_product is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

#         conn.commit()
#         logging.debug(f"Updated product: {updated_product}")

#         return {"Message": updated_product}
    
#     except (psycopg2.Error, Exception) as e:
#         conn.rollback()
#         logging.error(f"Error updating product: {e}")

   


# @app.delete("/product/{id}",status_code=status.HTTP_202_ACCEPTED)
# async def update_product(id : int ,response: Response,Dependcies:tuple=Depends(get_db_conn_cur)):
#     try :
#         conn=Dependcies[0]
#         cur=Dependcies[1]
#         cur.execute("""DELETE from products  where id =%s returning*; """,(id,))
#         update_product=cur.fetchone()
#         conn.commit()
#         logging.debug(f" Updated--{update_product}")
#         return {"Message":update_product}
#     except Exception as e:
#         logging.error(f"Error getting data from database {e}")
#         conn.rollback()
#         raise HTTPException(status_code=503,detail="Service Unavailable")


# @app.get("/users")
# async def user(Dependcies:tuple=Depends(get_db_conn_cur)):
#     try:
#         conn=Dependcies[0]
#         cur=Dependcies[1]
#         cur.execute("""SELECT * FROM users""")
#         users=cur.fetchall()
#         conn.commit()
#         logging.debug(f"Users Data Retreived Successfully: --{users}")

#         return { "Users": users }


#     except Exception as e:
#         logging.error(f"Error in fetching Users Details {e}")
#         raise  HTTPException(status_code=503,detail="Service Faild to Get  the Users")
    
# @app.post("/user")
# def add_user(user: schemas.user,Dependcies:tuple=Depends(get_db_conn_cur)):
#     try:
#         # Execute the SQL query to insert the new user
#         conn=Dependcies[0]
#         cur=Dependcies[1]
#         cur.execute(
#             "INSERT INTO users (username, password, role) VALUES (%s, %s, %s) RETURNING *;",
#             (user.username,hashing( user.password), user.role)
#         )
#         inserted_user = cur.fetchone()

#         conn.commit()
#         logging.error(f"User added successfully: {inserted_user}")
#         return {"Message": f"User added successfully {inserted_user}"}


#     except (psycopg2.Error, Exception) as e:
#         conn.rollback()
#         logging.error(f"Error adding user: {e}")
#         raise HTTPException(status_code=500, detail=str(e))
