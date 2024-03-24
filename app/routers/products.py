from fastapi import FastAPI, APIRouter,status,Depends,Response,HTTPException
from ..util import get_db_conn_cur
import logging
from app import schemas


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
def create_a_product(product:schemas.productCreate,response:Response,Dependcies:tuple=Depends(get_db_conn_cur)):
    """This is a POST request to create a new  product."""
    # logging.error(f'Data rom user:Payload received {product.model_dump_json()}-{response.status_code}')
    try:
        conn=Dependcies[0]
        cur=Dependcies[1]
        cur.execute("""INSERT INTO products (name, price, inventory) VALUES (%s, %s, %s) RETURNING name , price,inventory;""",
                   (product.name, product.price, product.inventory))
        product=cur.fetchone()
        conn.commit()
        logging.error(f'Data received  From DataBase: {product}-{response.status_code}')
        
        return {'Message': product}
    except Exception as e :
        logging.debug(f"Error in creating the data into table {e}")
        response.status_code=status.HTTP_406_NOT_ACCEPTABLE
        conn.rollback()
        return { "Error": str(e)}
    
    

@productRouter.put("/product/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_product(id: int, product: schemas.productUpdate, response: Response,Dependcies:tuple=Depends(get_db_conn_cur)):
    try:
        # Execute the SQL query to update the product
        conn=Dependcies[0]
        cur=Dependcies[1]
        cur.execute("""UPDATE products 
                        SET name = %s, price = %s, inventory = %s
                        WHERE id = %s 
                        RETURNING *;""",
                    (product.name, product.price, product.inventory, id))
        updated_product = cur.fetchone()

        if updated_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        conn.commit()
        logging.debug(f"Updated product: {updated_product}")

        return {"Message": updated_product}
    
    except Exception as e:
        conn.rollback()
        logging.error(f"Error updating product: {e}")

   


@productRouter.delete("/product/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_product(id : int ,response: Response,Dependcies:tuple=Depends(get_db_conn_cur)):
    try :
        conn=Dependcies[0]
        cur=Dependcies[1]
        cur.execute("""DELETE from products  where id =%s returning*; """,(id,))
        update_product=cur.fetchone()
        conn.commit()
        logging.debug(f" Updated--{update_product}")
        return {"Message":update_product}
    except Exception as e:
        logging.error(f"Error getting data from database {e}")
        conn.rollback()
        raise HTTPException(status_code=503,detail="Service Unavailable")
