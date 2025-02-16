from fastapi import FastAPI, Query, Header, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import uvicorn
import os

from schemas import RegUser, LoginUser, Task
import repository as rep
from cache import get_cached_user_id

app = FastAPI()

def check_auth(token: str) -> JSONResponse| str:
    user_id = get_cached_user_id(token)
    if not user_id:
        return JSONResponse(
            status_code=401,
            content={
                "status": "error", 
                "message": "Пользователь не авторизован."
            }
        )
        
    return user_id

@app.get("/api/ping")
def ping():
    return {"status": "ok"}

@app.post("/auth/sign-up")
def user_reg(item: RegUser):
    
    # if there is an error
    data = rep.reg_user(item)
    if isinstance(data, JSONResponse):
        return data
    
    return {"token": data}

@app.post("/auth/sign-in")
def user_login(item: LoginUser):
    
    # if there is an error
    data = rep.login_user(item)
    if isinstance(data, JSONResponse):
        return data
      
    return {"token": data}

@app.post("/api/todos")
def create_task(
    item: Task,
    token: str = Header(..., description="Authorization token", alias="Authorization")
    ):

    # auth
    check_res = check_auth(token)
    if isinstance(check_res, JSONResponse):
        return check_res
    else:
        user_id = check_res
    
    task = rep.create_task(item, user_id)
    return task

if __name__ == "__main__":
    load_dotenv()
    server_address = os.getenv("SERVER_ADDRESS")
    host, port = server_address.split(":")
    uvicorn.run("main:app", host=host, port=int(port), reload=True)
