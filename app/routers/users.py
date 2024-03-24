from fastapi import FastAPI, HTTPException, Response, status,APIRouter, Depends
import logging
from ..util import get_db_conn_cur,hashing
from app import schemas

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
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s) RETURNING *;",
            (user.username,hashing( user.password), user.role)
        )
        inserted_user = cur.fetchone()

        conn.commit()
        logging.error(f"User added successfully: {inserted_user}")
        return {"Message": f"User added successfully {inserted_user}"}


    except Exception as e:
        conn.rollback()
        logging.error(f"Error adding user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.put("/user/{id}")
async def update_user( id:int,user:schemas.user,Dependencies:tuple=Depends(get_db_conn_cur)):
   
    conn=Dependencies[0]
    cur=Dependencies[1]

    try:
        cur.execute("""UPDATE users SET username=%s ,password=%s,role=%s WHERE seller_id=%s returning username,role,seller_id;""", 
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
async def update_user( id:int,Dependencies: tuple=Depends(get_db_conn_cur)):


   
    conn=Dependencies[0]
    cur=Dependencies[1]

    try:
        cur.execute("""SELECT username,role,seller_id
                        FROM users
                        WHERE seller_id = %s
                        """, 
                    (id,))
        updated_user=dict(cur.fetchone() )
        conn.commit()
        logging.error(f"<--The user exists Details---")
        return {"Message":f"The user {updated_user.get('username')}-{updated_user} exists"}
    except Exception as e:
        conn.rollback()
        logging.error(f"Failed to update user: {e}")
        raise  HTTPException(status_code=404,detail=f"{e}")
    
    




@userRouter.delete("/user/{id}")
async def update_user( id:int,Dependencies: tuple=Depends(get_db_conn_cur)):
    
   
    conn=Dependencies[0]
    cur=Dependencies[1]

    try:
        cur.execute("""DELETE 
                        FROM users
                        WHERE seller_id = %s RETURNING  *;""", 
                        
                    (id,))
        deleted_user=dict(cur.fetchone() )
        conn.commit()
        logging.error(f"<--The user {deleted_user} Deteleted loggs---")
        return {"Message":f"The user {deleted_user.get('username')}-{deleted_user} Deleted succesfully"}
    except Exception as e:
        conn.rollback()
        logging.error(f"Failed to update user: {e}")
        raise  HTTPException(status_code=404,detail=f"{e}")