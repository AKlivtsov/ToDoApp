# database
from database import engine, User, Task
from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

#schemas
from schemas import RegUser, LoginUser
from schemas import Task as TaskSchm

#cache
from cache import cache_token

# errors
from fastapi.responses import JSONResponse

# security
import hashlib
from uuid import uuid4

def reg_user(user: RegUser) -> str | JSONResponse:
    with Session(engine) as session:
        with session.begin():
            user_data = user.model_dump()
            
            # check if email already exists
            email = session.scalar(select(User.email).where(User.email == user_data['email']))
            if email:
                return JSONResponse(
                    status_code=400, 
                    content={
                        "status": "error",
                        "message": "Такой email уже зарегистрирован"
                    }
                )
            
            # to db
            user_data['password'] = hashlib.sha3_224(user_data["password"].encode()).hexdigest()
            new_user = User(**user_data) # adding username, email, hash of password
            session.add(new_user)
            
            # to cache
            session.flush()
            token = str(uuid4())
            cache_token(new_user.id, token)
            
            return token
        
def login_user(user: LoginUser) -> str | JSONResponse:
    with Session(engine) as session:
        with session.begin():
            user_data = user.model_dump()
            user_data['password'] = hashlib.sha3_224(user_data["password"].encode()).hexdigest()
            
            # auth
            password = session.scalar(select(User.password).where(User.email == user_data['email']))
            if password != user_data['password'] or not password:
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "error",
                        "message": "Неверный email или пароль."
                    }
                )
            
            # cache
            user_id = session.scalar(select(User.id).where(User.email == user_data['email']))
            token = str(uuid4())
            cache_token(user_id, token)
            
            return token
        
def create_task(task: TaskSchm, user_id: str) -> list | JSONResponse:
    with (Session(engine) as session):
        with session.begin():
            task_data = task.model_dump()

            task_data['user_fk'] = user_id
            new_task = Task(**task_data) # adding title, desc, user_fk
            session.add(new_task)
            session.flush()

            task_id = new_task.id
            session.commit()
    
    return {"id": task_id, "title": task_data["title"], "description": task_data["description"]}
