from fastapi import FastAPI, HTTPException, Response, status,APIRouter, Depends
import logging
from ..util import get_db_conn_cur,hashing
from app import schemas
from app.oauth2 import get_current_user 
from datetime import datetime



logging.basicConfig(level=logging.ERROR,format='----->%(asctime)s - %(name)s - %(message)s ') 



purchaseRouter=APIRouter(tags=["Purchasing"])



@purchaseRouter.put("/deposit")
async def deposit(deposit:schemas.deposit,Dependcies:tuple=Depends(get_db_conn_cur),current_user=Depends(get_current_user)):
    logging.error(f"----------------=================CurrentUser=============== {current_user}")
    try:
       
        if  current_user['role'] != 'buyer':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Only buyer can deposit money.")
            
        conn=Dependcies[0]
        cur=Dependcies[1]
        cur.execute("""UPDATE users SET deposit=%s  WHERE id=%s returning username,role,id,deposit;""",(deposit.deposit,current_user['id']))
        deposit=cur.fetchone()
        conn.commit()
        logging.error(f"Users Data Retreived Successfully: --{deposit}")

        return { "User deposit": deposit }


    except Exception as e:
        logging.error(f"Error in fetching Users Details {e}")
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Only buyer can deposit money.")
    
@purchaseRouter.get("/reset")
async def reset(Dependcies:tuple=Depends(get_db_conn_cur),current_user=Depends(get_current_user)):
    logging.error(f"----------------=================CurrentUser=============== {current_user}")
    try:
       
        if  current_user['role'] != 'buyer':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Only buyer can deposit money.")
            
        conn=Dependcies[0]
        cur=Dependcies[1]

        cur.execute("""select deposit from users  WHERE id=%s  ;""",(current_user['id'],))
        old_deposit=dict(cur.fetchone())['deposit']
        # reset_deposit=0
        cur.execute("""UPDATE users SET deposit=0  WHERE id=%s returning username,role,id,deposit;""",(current_user['id'],))
        conn.commit()
        current_deposit=dict(cur.fetchone())['deposit']

        logging.error(f"Users Data Retreived Successfully: --{current_deposit}")

        return { "Current deposit": current_deposit,"Returned Deposit":old_deposit }


    except Exception as e:
        logging.error(f"Error in fetching Users Details {e}")
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Only buyer can deposit money.")
    

@purchaseRouter.post('/buy')
def makePurchase(order:schemas.order,Dependcies:tuple=Depends(get_db_conn_cur),current_user=Depends(get_current_user)):

 
    logging.error(f"----------------=================CurrentUser=============== {current_user}")
    
    conn = Dependcies[0]
    cur = Dependcies[1]
    try:   
        if  current_user['role'] != 'buyer':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Only buyer can deposit money.")
        cur.execute('''SELECT * FROM products WHERE id=%s ''',(order.product_id,))
        dataProduct = dict(cur.fetchone())
        logging.error(dataProduct)



        cur.execute("""SELECT * FROM users WHERE id=%s""",(current_user['id'],))
        dataBuyer = dict(cur.fetchone())
        logging.error(dataBuyer)

        if not dataProduct:
            raise ValueError("Invalid product ID ")
        if dataBuyer['deposit'] < dataProduct['price']*order.product_quantity:
            raise ValueError("please Deposit Enough Money ")

        if dataProduct["inventory"] < order.product_quantity:
                raise ValueError("Not enough stock for this product")   
                
        else:
              updated_inventory=dataProduct["inventory"]-order.product_quantity  
              remainingMoney=dataBuyer['deposit']-dataProduct['price']*order.product_quantity
              cur.execute("""UPDATE products SET inventory=%s WHERE id=%s""" , (updated_inventory,order.product_id))  
              cur.execute("""UPDATE users SET deposit=0 WHERE id=%s""" , (current_user['id'],))  
              conn.commit()
              order={
                      'current_user_id':current_user['id'],
                      'product_id':order.product_id,
                      'quantity':order.product_quantity,
                      'total_order_price':dataProduct['price']*order.product_quantity,
                      'Returned_Money':remainingMoney,
                      'product_price':dataProduct['price'],
                      'date':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                       }
              
              logging.error( f'Order =============>{order} ')
              return {'message':'Order Placed Successfully','Data':order}
          
    except Exception as e:
        conn.rollback()
        return{'message': str(e)}