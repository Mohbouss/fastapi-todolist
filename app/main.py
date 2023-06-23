from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor  
import time
app = FastAPI()

class Post(BaseModel):
    description: str
    UserId: int
class UpdateTask(BaseModel):
    description:str
##CONNECTION WITH DB
while True:
   try:
      conn= psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='123456', cursor_factory=RealDictCursor)
      cursor = conn.cursor()
      print('datatbse connc was success')
      break
   except Exception as error:
      print("connec failed")
      print('error:',error)
      time.sleep(2)








##task CRUD

##read tasks
@app.get('/tasks')
def read_tasks():
 cursor.execute("""Select * from tasks""")
 tasks=cursor.fetchall()
 return {"data":tasks}   

##create tasks
@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_tasks(task: Post):
    cursor.execute("""insert into tasks(description,user_id) values(%s,%s)returning * """,(task.description,task.UserId))
    new_task= cursor.fetchone()
    conn.commit()
    return {"data":new_task}

##update task
@app.put('/tasks/{id}',status_code=status.HTTP_200_OK)
def update_tasks(id: int,task:UpdateTask):
    cursor.execute("""update tasks set description = %s where id = %s returning * """,(task.description,str(id)))
    updated_task  =cursor.fetchone()
    if not updated_task :
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"task with id: {id} not found")
    conn.commit()   
    return {'data':updated_task}
##delete task

@app.delete('/tasks/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    cursor.execute("""delete from tasks where id = %s returning * """, (str(id),))
    deleted_task= cursor.fetchone()
    conn.commit()
    if not deleted_task:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"task with id: {id} not found")
   
    return Response(status_code=status.HTTP_204_NO_CONTENT)

####USER CRUD 

## read users
@app.get('/users')
def  read_user():
   cursor.execute("select * from users ")
   readed_users=cursor.fetchall()
   return {"data :": readed_users}
