from fastapi import FastAPI, HTTPException, Response, status,APIRouter, Depends
import logging
from ..util import get_db_conn_cur,hashing
from app import schemas
from app.oauth2 import get_current_user 

logging.basicConfig(level=logging.ERROR,format='----->%(asctime)s - %(name)s - %(message)s ') 



userRouter=APIRouter(tags=["Users"])



@userRouter.get("/users")
async def user(Dependcies:tuple=Depends(get_db_conn_cur)):
    try:
        conn=Dependcies[0]
        cur=Dependcies[1]
        cur.execute("""SELECT * FROM users""")
        users=cur.fetchall()
        conn.commit()
        logging.debug(f"Users Data Retreived Successfully: --{users}")

        return { "Users": users }


    except Exception as e:
        logging.error(f"Error in fetching Users Details {e}")
        raise  HTTPException(status_code=503,detail="Service Faild to Get  the Users")
    
@userRouter.post("/signUp")
def add_user(user: schemas.user,Dependcies:tuple=Depends(get_db_conn_cur)):
    try:
        # Execute the SQL query to insert the new user
        conn=Dependcies[0]
        cur=Dependcies[1]
        cur.execute(
            "INSERT INTO users (username, password, role, deposit) VALUES (%s, %s, %s, %s) RETURNING *;",
            (user.username,hashing(user.password), user.role,user.deposit))
        
        inserted_user = cur.fetchone()

        conn.commit()
        logging.error(f"User added successfully: {inserted_user}")
        return {"Message": f"User added successfully {inserted_user}"}


    except Exception as e:
        conn.rollback()
        logging.error(f"Error adding user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.put("/user/{id}")
async def update_user( id:int,user:schemas.user,Dependencies:tuple=Depends(get_db_conn_cur),current_user:dict=Depends(get_current_user)):
    logging.error(f"----------------=================CurrentUser=============== {current_user}")
    conn=Dependencies[0]
    cur=Dependencies[1]

    try:
        if current_user['role']!='seller':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized to access this data")
        cur.execute("""UPDATE users SET username=%s ,password=%s,role=%s WHERE id=%s returning username,role,id;""", 
                    (user.username,hashing(user.password),user.role,id))
        updated_user= dict(cur.fetchone())
        conn.commit()
        logging.error(f"---The user has been Updated,Details---{updated_user}")
        return {"Message":f"The user has been Updated {updated_user}"}
    except Exception as e:
        conn.rollback()
        logging.error(f"Failed to update user: {e}")
        raise  HTTPException(status_code=404,detail=f"{e}")
    



@userRouter.get("/user/{id}")
async def get_user( id:int,Dependencies: tuple=Depends(get_db_conn_cur),current_user:dict=Depends(get_current_user)):
    logging.error(f"----------------=================CurrentUser=============== {current_user}")


   
    conn=Dependencies[0]
    cur=Dependencies[1]

    try:
        if current_user['role']!='seller':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized to access this data")
        cur.execute("""SELECT username,role,id
                        FROM users
                        WHERE id = %s
                        """, 
                    (id,))
        get_user=dict(cur.fetchone() )
        conn.commit()
        logging.error(f"<--The user exists Details---")
        return {"Message":f"The user {get_user.get('username')}-{get_user} exists"}
    except Exception as e:
        conn.rollback()
        logging.error(f"Failed to get user: {e}")
        raise  HTTPException(status_code=404,detail=f"{e}")
    
    




@userRouter.delete("/user/{id}")
async def delete_user( id:int,Dependencies: tuple=Depends(get_db_conn_cur),current_user:dict=Depends(get_current_user)):
    logging.error(f"----------------=================CurrentUser=============== {current_user}")
    
   
    conn=Dependencies[0]
    cur=Dependencies[1]

    try:
        if current_user['role']!='seller':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized to access this data")
        cur.execute("""DELETE 
                        FROM users
                        WHERE id = %s RETURNING  *;""", 
                        
                    (id,))
        deleted_user=dict(cur.fetchone() )
        conn.commit()
        logging.error(f"<--The user {deleted_user} Deteleted loggs---")
        return {"Message":f"The user {deleted_user.get('username')}-{deleted_user} Deleted succesfully"}
    except Exception as e:
        conn.rollback()
        logging.error(f"Failed to update user: {e}")
        raise  HTTPException(status_code=404,detail=f"===={e}")