# database
from database import engine, User, Task
from sqlalchemy import func, select, update, delete, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# api
from flask import Flask, request
# TODO: add flask-limiter !!!

# security
import hashlib
from uuid import uuid4


app = Flask(__name__)

def check_token_from_header():
    token = fr"{request.headers}".split("Token: ")[1].split("\r")[0]

    # cheking the token
    with (Session(engine) as session):
        with session.begin():
            token = session.scalar(select(User.token).where(User.token == token))
    
    return token

def check_authorship(token, task_id):
    with (Session(engine) as session):
        with session.begin():
            user_id = session.scalar(select(User.id).where(User.token == token))
            task_user_fk = session.scalar(select(Task.user_fk).where(Task.id == task_id))

    if user_id != task_user_fk:
        return False
    
    return True

# --- users

@app.post("/api/register")
def register():
    data = request.get_json()
    token = str(uuid4())

    try:
        # trying to register user
        with (Session(engine) as session):
            with session.begin():
                user = User(
                    username = data["name"],
                    password = hashlib.sha3_224(data["password"].encode()).hexdigest(),
                    email = data["email"],
                    token = token
                    )
                session.add(user)
            session.commit()

    except IntegrityError as e:
        # get the reason by striping error msg
        reason = str(e).split('failed:')[1].split('[')[0][7:-1]
        return {'error': f'{reason} already exists'}, 409

    return {'token': token}, 201

@app.get("/api/login")
def login():
    data = request.get_json()
    condition = and_(
        User.email == data["email"], 
        User.password == hashlib.sha3_224(data["password"].encode()).hexdigest()
        )

    with (Session(engine) as session):
        with session.begin():
            token = session.scalar(select(User.token).where(condition))
                
    if not token:
        return {'error': 'User not found'}, 401
    
    return {'token': token}, 200

# --- tasks

@app.post("/api/todos")
def create_task():
    data = request.get_json()

    #check authorization
    valid_token = check_token_from_header()

    if not valid_token:
        return {"message": "Unauthorized"}, 401
    
    # if all good, create task
    with (Session(engine) as session):
        with session.begin():
            user_id = session.scalar(select(User.id).where(User.token == valid_token))
            task = Task(
                name = data["title"],
                description = data["description"],
                user_fk = user_id
            )
            session.add(task)
            session.flush()

            task_id = task.id
            session.commit()
    
    return {"id": task_id, "title": data["title"], "description": data["description"]}, 201

@app.put("/api/todos/<int:task_id>")
def update_task(task_id):
    data = request.get_json()

    #check authorization
    valid_token = check_token_from_header()

    if not valid_token:
        return {"message": "Unauthorized"}, 401

    # checking authorship
    if not check_authorship(valid_token, task_id):
        return {"message": "Forbidden"}, 403
    
    # if all good, update task
    with (Session(engine) as session):
        with session.begin():
            session.execute(
                update(Task)
                .where(Task.id == task_id)
                .values(name = data["title"], description = data["description"])
                )
            
            session.commit()

    return {"id": task_id, "title": data["title"], "description": data["description"]}, 200

@app.delete("/api/todos/<int:task_id>")
def delete_task(task_id):
    #check authorization
    valid_token = check_token_from_header()

    if not valid_token:
        return {"message": "Unauthorized"}, 401

    # checking authorship
    if not check_authorship(valid_token, task_id):
        return {"message": "Forbidden"}, 403
    
    #if all good, delete task
    with (Session(engine) as session):
        with session.begin():
            session.execute(delete(Task).where(Task.id == task_id))
            session.commit()
    
    return {}, 204

@app.get("/api/todos")
def get_task():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))

    #check authorization
    valid_token = check_token_from_header()

    if not valid_token:
        return {"message": "Unauthorized"}, 401
    
    # get user id
    with (Session(engine) as session):
        with session.begin():
            user_id = session.scalar(select(User.id).where(User.token == valid_token))

    #if all good, get tasks
    tasks = []
    with (Session(engine) as session):
        with session.begin():
            ids = session.scalars(
                select(Task.id, Task.name, Task.description)
                .where(Task.user_fk == user_id)
                .offset(limit*(page-1)).limit(limit)
                ).all()

            for id in ids:
                title = session.scalar(select(Task.name).where(Task.id == id))
                desc = session.scalar(select(Task.description).where(Task.id == id))
                tasks.append({"id": id, "title": title, "description": desc})

    return {"page": page, "limit": limit, "total": len(tasks), "data": tasks}, 200

# --- errors 

@app.errorhandler(404)
def not_found(error):
    return {"error": "Data not found"}, 404

@app.errorhandler(500)
def internal_server_error(error):
    return {"error": "Internal Server Error"}, 500


if __name__ == '__main__':
    app.run()
