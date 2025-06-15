# database
from database import engine, User, Task
from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# schemas
from schemas import RegUser, LoginUser
from schemas import Task as TaskSchm

# cache
from cache import cache_token

# errors
from fastapi.responses import JSONResponse

# security
import hashlib
from uuid import uuid4


def check_authorship(user_id: str, task_id: str) -> bool:
    with Session(engine) as session:
        with session.begin():
            task_fk = session.scalar(select(Task.user_fk).where(Task.id == task_id))

    if user_id != task_fk:
        return False

    return True


def reg_user(user: RegUser) -> None | str:
    with Session(engine) as session:
        with session.begin():
            user_data = user.model_dump()

            # check if email already exists
            email = session.scalar(
                select(User.email).where(User.email == user_data["email"])
            )
            if email:
                return None

            # to db
            user_data["password"] = hashlib.sha3_224(
                user_data["password"].encode()
            ).hexdigest()
            new_user = User(**user_data)  # adding username, email, hash of password
            session.add(new_user)

            # to cache
            session.flush()
            token = str(uuid4())
            cache_token(new_user.id, token)

            return token


def login_user(user: LoginUser) -> None | str:
    with Session(engine) as session:
        with session.begin():
            user_data = user.model_dump()
            user_data["password"] = hashlib.sha3_224(
                user_data["password"].encode()
            ).hexdigest()

            # auth
            password = session.scalar(
                select(User.password).where(User.email == user_data["email"])
            )
            if password != user_data["password"] or not password:
                return None

            # cache
            user_id = session.scalar(
                select(User.id).where(User.email == user_data["email"])
            )
            token = str(uuid4())
            cache_token(user_id, token)
            print(user_id)

            return token


def create_task(task: TaskSchm, user_id: str) -> str:
    with Session(engine) as session:
        with session.begin():
            task_data = task.model_dump()

            task_data["user_fk"] = user_id
            new_task = Task(**task_data)  # adding title, desc, user_fk
            session.add(new_task)
            session.flush()

            task_id = new_task.id
            session.commit()

    return task_id, task_data["title"], task_data["description"]


def update_task(task: TaskSchm, task_id: int) -> str:
    with Session(engine) as session:
        with session.begin():
            task_data = task.model_dump()
            session.execute(update(Task).where(Task.id == task_id).values(**task_data))

            session.commit()

    return task_id, task_data["title"], task_data["description"]


def delete_task(task_id: str, user_id: str) -> bool:
    try:
        with Session(engine) as session:
            with session.begin():
                session.execute(delete(Task).where(Task.id == task_id))

                session.commit()

        return True

    except Exception as e:
        print(e)  # do some logging here!!!
        return False


def get_tasks(user_id: str, limit: int, page: int) -> list:
    with Session(engine) as session:
        with session.begin():
            tasks = []
            ids = session.scalars(
                select(Task.id, Task.title, Task.description)
                .where(Task.user_fk == user_id)
                .offset(limit * (page - 1))
                .limit(limit)
            ).all()

            for id in ids:
                title = session.scalar(select(Task.title).where(Task.id == id))
                desc = session.scalar(select(Task.description).where(Task.id == id))
                tasks.append({"id": id, "title": title, "description": desc})

    return tasks


def add_friend(user_id: str, friend_id: str) -> bool:
    if friend_id == user_id:
        return False

    with Session(engine) as session:
        with session.begin():
            friend = session.scalar(select(User).where(User.id == int(friend_id)))
            if friend is None:
                return False
            user = session.scalar(select(User).where(User.id == user_id))

            if friend in user.following:
                return True

            user.following.append(friend)
            session.commit()
            return True


def accept_friend(user_id: str, friend_id: str) -> bool:
    if friend_id == user_id:
        return False

    with Session(engine) as session:
        with session.begin():
            user = session.scalar(select(User).where(user_id == user_id))
            friend_folowing = session.scalar(
                select(User.following).where(user_id == friend_id)
            )
            if user not in friend_folowing:
                return False

            friend = session.scalar(select(User).where(user_id == friend_id))
            user.following.append(friend)
            session.commit()
            return True


def get_awaitingFriends(user_id: str) -> list:
    with Session(engine) as session:
        with session.begin():
            user = session.scalar(select(User).where(user_id == user_id))

            awaiting_list = []
            for person in user.followers:
                if person not in user.following:
                    awaiting_list.append({"username": person.username, "id": person.id})

            return awaiting_list


def get_friends_tasks(user_id: str, limit: int, page: int) -> list:
    with Session(engine) as session:
        with session.begin():
            user = session.scalar(select(User).where(User.id == user_id))
            friends = []

            for person in user.following:
                if person in user.followers:
                    friends.append(person.id)

            for friend_id in friends:

                tasks = []
                ids = session.scalars(
                    select(Task.id, Task.title, Task.description)
                    .where(Task.user_fk == friend_id)
                    .offset(limit * (page - 1))
                    .limit(limit)
                ).all()

                for id in ids:
                    title = session.scalar(select(Task.title).where(Task.id == id))
                    desc = session.scalar(select(Task.description).where(Task.id == id))
                    tasks.append({"id": id, "title": title, "description": desc})

    return tasks
