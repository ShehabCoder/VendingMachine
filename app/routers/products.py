from fastapi import FastAPI, APIRouter,status,Depends,Response,HTTPException
from ..util import get_db_conn_cur
import logging
from app import schemas
from app.oauth2 import get_current_user


logging.basicConfig(level=logging.ERROR,format='----->%(asctime)s - %(name)s - %(message)s ') 



productRouter=APIRouter(tags=["Products"])




@productRouter.get("/products")
async def read_root(Dependcies:tuple=Depends(get_db_conn_cur)):
    try:
        conn=Dependcies[0]
        cur=Dependcies[1]
        cur.execute("""SELECT * FROM products """)
        products=cur.fetchall()
        conn.commit()
        logging.debug("Products Fetched Succesfully")

        return {"message": products }

    except Exception as e:
        logging.error("Faild To Fetch Data  From DB",exc_info=True)
        conn.rollback()
        return {"Error":str(e)}



@productRouter.post("/product",status_code=status.HTTP_201_CREATED)
def create_a_product(product:schemas.productCreate,response:Response,Dependcies:tuple=Depends(get_db_conn_cur),current_user:dict=Depends(get_current_user)):
    """This is a POST request to create a new  product."""
    # logging.error(f'Data rom user:Payload received {product.model_dump_json()}-{response.status_code}')
    logging.error(f"----------------=================CurrentUser=============== {current_user}")
    conn=Dependcies[0]
    cur=Dependcies[1]
    try:
        if current_user['role']!='seller':
            raise HTTPException(status_code=403,detail="Only Sellers can Create Products ")
        cur.execute("""INSERT INTO products (name, price, inventory,seller_id) VALUES (%s, %s, %s,%s) RETURNING *;""",
            (product.name, product.price, product.inventory,current_user['id']))
        product=cur.fetchone()
        conn.commit()
        logging.error(f'Data received  From DataBase: {product}-{response.status_code}')
        
        return {'Message': product}
    except Exception as e :
        logging.debug(f"Error in creating the data into table {e}")
        conn.rollback()
        return { "MESSAGE": str(e)}
    
    

@productRouter.put("/product/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_product(id: int, product: schemas.productUpdate, response: Response,Dependcies:tuple=Depends(get_db_conn_cur),current_user:dict=Depends(get_current_user)):
    conn=Dependcies[0]
    cur=Dependcies[1]
    try:
        # Execute the SQL query to update the product
        if current_user['role']!="seller":
            raise HTTPException(status_code = 403 , detail ="You are not authorized for this action")
        cur.execute("""UPDATE products 
                        SET name = %s, price = %s, inventory = %s,seller_id=%s
                        WHERE id = %s 
                        RETURNING *;""",
                    (product.name, product.price, product.inventory,current_user['id'] ,id))
        updated_product = cur.fetchone()

        if updated_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        conn.commit()
        logging.debug(f"Updated product: {updated_product}")

        return {"Message": updated_product}
    
    except Exception as e:
        conn.rollback()
        logging.error(f"Error updating product: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized to perform this action")

   


@productRouter.delete("/product/{id}")
async def delete_product(id : int ,Dependcies:tuple=Depends(get_db_conn_cur),current_user:dict=Depends(get_current_user)):
    logging.error(f"----------------=================CurrentUser=============== {current_user}")
    cur=Dependcies[1]
    conn=Dependcies[0]
    # try:
           
    #     cur.execute("""SELECT * from products  where seller_id =%s ;""",(current_user['id'],))
    #     product=cur.fetchone()
    #     conn.commit()
        
    #     # seller_id=dict(product)['seller_id']
    #     # logging.error(f" Get Seller_id --{product}")
    #     if product == None :
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You are a seller but  dont Have products to delete")
    #     # seller_id=int(dict(cur.fetchone())['seller_id'])
    # except Exception as e:
    #     logging.error(f"Error getting product info for delete : {e}")
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"-{e}")
        

    try :
        # if current_user['id'] != seller_id:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Only Sellers Who  Create this Product can delete ")
        if current_user['role']!='seller' :
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Only Sellers can Delete Products ")
        cur.execute("""DELETE from products  where id =%s AND seller_id =%s returning*; """,(id,current_user['id']))
        conn.commit()
        deleted_product=cur.fetchone()
        if cur.rowcount==0 :
            raise HTTPException(status_code=422,detail="This Product does not exist in your stock to Delete.")
        conn.commit()
        logging.error(f" Deleted Product--{deleted_product}")
        return {"Message":deleted_product}
    except Exception as e:
        logging.error(f"Error Deleting data from database {str(e)}")
        conn.rollback()
        raise HTTPException(status_code=401,detail=f"{str(e)}")



