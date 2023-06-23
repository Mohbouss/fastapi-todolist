from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor  
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    description: str
    UserId: int
class UpdateTaskDescription(BaseModel):
    description: str

class UpdateTaskState(BaseModel):
    completed: bool
class User(BaseModel):
    name:  str

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
def get_all_tasks():
 cursor.execute("""Select * from tasks order by id""")
 tasks=cursor.fetchall()
 return list(tasks)  
##read task with specific id 
@app.get('/tasks/{id}/state')
def get_task_state(id :int):
 cursor.execute("""Select completed from tasks where id = %s  order by id """,(str(id),))
 state=cursor.fetchone()
 return state  
##create tasks
@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(task: Post):
    cursor.execute("""insert into tasks(description,user_id) values(%s,%s)returning * """,(task.description,task.UserId))
    new_task= cursor.fetchone()
    conn.commit()
    return new_task

##update task description
@app.put('/tasks/{id}/description',status_code=status.HTTP_200_OK)
def update_task_description(id: int,task:UpdateTaskDescription):
    cursor.execute("""update tasks set description = %s where id = %s returning * """,(task.description,str(id),))
    updated_task  =cursor.fetchone()
    if not updated_task :
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"task with id: {id} not found")
    conn.commit()   
    return updated_task
##update task state
@app.put('/tasks/{id}/state',status_code=status.HTTP_200_OK)
def update_task_state(id: int,task:UpdateTaskState):
    cursor.execute("""update tasks set completed = %s where id = %s returning *  """,(task.completed,str(id),))
    updated_task  =cursor.fetchone()
    if not updated_task :
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"task with id: {id} not found")
    conn.commit()   
    return updated_task
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
def  get_all_users():
   cursor.execute("select * from users order by id  ")
   readed_users=cursor.fetchall()
   return  readed_users
@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(user : User):
    cursor.execute("""insert into users(name) values(%s) returning * """,(user.name,))
    new_user= cursor.fetchone()
    conn.commit()
    return new_user

@app.delete('/users/{id}')
def delete_user(id :int):
   cursor.execute("delete from users where id =%s returning *",(str(id),))
   deleted_user= cursor.fetchone()
   conn.commit()
   if not deleted_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id : {id} not found")
   
   return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/users/{id}")
def get_user_information(id : int ):
    cursor.execute("""select * from users where id = %s   """,(str(id),))
    tasks= cursor.fetchall()
    return tasks

@app.get("/users/{id}/tasks")
def get_task_specified_user(id : int ):
    cursor.execute("""select * from tasks where user_id =%s order by id  """,(str(id),))
    tasks= cursor.fetchall()
    return tasks

    