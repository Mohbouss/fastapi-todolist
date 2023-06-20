from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from random import randrange
app = FastAPI()
 
class Post(BaseModel):
    task: str
    completed: bool
class UpdateTask(BaseModel):
    task:str
    completed: bool
    id :int
 
my_tasks = [{"task" :"study fastapi", "completed":False , "id": 1},{"task" :"complete fastapi", "completed":False , "id":2}]
 
def find_task(id):
   for p in my_tasks:
      if p['id'] == id:
        return my_tasks.index(p)
 
#@app.get("/")
#async def root():
#    return {"message": "Hello mohamed "}
#@app.get("/posts")
#def get_posts():
 #   return{'data':"this is your post"}
#@app.post("/createposts")
#def  post_mypost(new_post : Post):
#    print(new_post)
#    return {'data':'new post'}
@app.get('/readtasks')
def read_tasks():
 return {"data":my_tasks}   
@app.post('/createtasks', status_code=status.HTTP_201_CREATED)
def create_tasks(task: Post):
    task_dict = task.dict()
    task_dict["id"] = randrange(0,10000000)
    my_tasks.append(task_dict)
    print(my_tasks)
 
    return {'data':task_dict}
@app.put('/updatetask/{id}')
def update_tasks(id: int,task:UpdateTask):
    index =find_task(id)
 
    task_dict =task.dict()
    my_tasks[index] =task_dict
    return {'data':task_dict}
@app.delete('/deletetask/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    ind=find_task(id)
    my_tasks.pop(ind)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
