# database
from database import engine, User, Task
from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def register_user(username: str, password: str, email: str) -> bool | dict:
    try:
        # trying to register user
        with (Session(engine) as session):
            with session.begin():
                user = User(
                    username = username, 
                    password = password, 
                    email = email,
                    )
                session.add(user)
            session.commit()

    except IntegrityError as e:
        # get the reason by striping error msg
        reason = str(e).split('failed:')[1].split('[')[0][7:-1]
        return False, {'error': f'{reason} already exists'}
    
    return True