from fastapi import FastAPI, Query, Header, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import uvicorn
import os

from schemas import RegUser, LoginUser, Task
import repository as rep
from cache import get_cached_user_id

app = FastAPI()

@app.get("/api/ping")
def ping():
    return {"status": "ok"}

@app.post("/auth/sign-up")
def api_user_reg(
    item: RegUser
    ):
    token = rep.reg_user(item)

    if token is None:
        return JSONResponse(
            status_code=400, 
            content={
                "status": "error",
                "message": "Такой email уже зарегистрирован"
                }
            )

    return {"token": token}

@app.post("/auth/sign-in")
def api_user_login(
    item: LoginUser
    ):
    token = rep.login_user(item)

    if token is None:
        return JSONResponse(
            status_code=400, 
            content={
                "status": "error",
                "message": "Неверный email или пароль"
                }
            )
      
    return {"token": token}

@app.post("/api/todos")
def api_create_task(
    item: Task,
    token: str = Header(..., description="Authorization token", alias="Authorization")
    ):

    # auth
    user_id = get_cached_user_id(token)
    if not user_id:
        return JSONResponse(
            status_code=401,
            content={
                "status": "error", 
                "message": "Пользователь не авторизован."
            }
        )
    
    id_, title, desc = rep.create_task(task=item, user_id=user_id)
    return {
        "id": id_,
        "title": title,
        "description": desc
        }

@app.put( "/api/todos/{task_id}")
def api_update_task(
    task_id:int,
    item: Task,
    token: str = Header(..., description="Authorization token", alias="Authorization")):

    # auth
    user_id = get_cached_user_id(token)
    if not user_id:
        return JSONResponse(
            status_code=401,
            content={
                "status": "error", 
                "message": "Пользователь не авторизован."
            }
        )

    # check authorship
    check = rep.check_authorship(user_id=user_id, task_id=task_id)
    if check:
        return JSONResponse(
            status_code=403, 
            content={
                "status": "error",
                "message": "Вы не являетесь автором задачи."
            }
        )
    
    id_, title, desc = rep.update_task(task_id=task_id, task=item)
    return {
        "id": id_,
        "title": title,
        "description": desc
        }

@app.delete("/api/todos/{task_id}", status_code=204)
def api_delete_task(
    task_id:int,
    token: str = Header(..., description="Authorization token", alias="Authorization")):

    # auth
    user_id = get_cached_user_id(token)
    if not user_id:
        return JSONResponse(
            status_code=401,
            content={
                "status": "error", 
                "message": "Пользователь не авторизован."
            }
        )
    
    # check authorship
    check = rep.check_authorship(user_id=user_id, task_id=task_id)
    if check:
        return JSONResponse(
            status_code=403, 
            content={
                "status": "error",
                "message": "Вы не являетесь автором задачи."
            }
        )
    
    is_succses = rep.delete_task(task_id=task_id, user_id=user_id)
    if is_succses:
        return Response(status_code=204)
    
    return Response(status_code=500)

@app.get("/api/todos")
def api_get_tasks(
    token: str = Header(..., description="Authorization token", alias="Authorization"),
    page: str = Query(..., description="page", alias="Page"),
    limit: str = Query(..., description="limit of the items", alias="Limit"
    )):

    # auth
    user_id = get_cached_user_id(token)
    if not user_id:
        return JSONResponse(
            status_code=401,
            content={
                "status": "error", 
                "message": "Пользователь не авторизован."
            }
        )

    tasks = rep.get_tasks(user_id=user_id, limit=int(limit), page=int(page))
    return {
        "page": page,
        "limit": limit,
        "total": len(tasks),
        "data": tasks
        }


if __name__ == "__main__":
    load_dotenv()
    server_address = os.getenv("SERVER_ADDRESS")
    host, port = server_address.split(":")
    uvicorn.run("main:app", host=host, port=int(port))
