# web stuff
import reflex as rx 

# api
import requests as re
from requests import Response

# database
from webClient.database.database import engine, User
from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def add_user_to_db(username: str, email: str, token: str):
    with (Session(engine) as session):
        with session.begin():
            session.execute(delete(User))
            user = User(username=username, email=email, token=token)
            session.add(user)
            session.commit()

def get_token() -> str:
    with (Session(engine) as session):
        with session.begin():
            token = session.scalar(select(User.token))
    
    return token


class SettingState(rx.State):
    # use .set for change vars
    _url: str = "http://127.0.0.1:5000/api/"


class UserState(rx.State):

    @rx.event
    def handle_registration(self, form_data: dict):
        try:
            res: Response = re.post(SettingState._url + "register", json=form_data)
            if res.status_code == 201:
                add_user_to_db(form_data["name"], form_data["email"], res.json()['token'])

        except Exception as e:
            print(f"An error occured from {__class__}: {e}")

    @rx.event
    def handle_login(self, form_data: dict):
        try:
            res: Response = re.get(SettingState._url + "login", json=form_data)
            if res.status_code == 200:
                add_user_to_db(res.json()["name"], form_data["email"], res.json()['token'])

        except Exception as e:
            print(f"An error occured from {__class__}: {e}")
    

class TaskState(rx.State):
    
    @rx.var
    def tasks(self) -> list[dict[str, str | int]]:
        try:
            res: Response = re.get(
                SettingState._url + "todos",
                params={"page": 1, "limit": 999},
                headers={"Token": get_token()}
                )
            if res.status_code == 200:
                return res.json()["data"]

        except Exception as e:
            print(f"An error occured from {__class__}: {e}")

    @rx.event
    def handle_edit(self, form_data: dict):
        try:
            re.put(
                SettingState._url + f"todos/{form_data["id"]}",
                headers={"Token": get_token()},
                json=form_data,
            )

        except Exception as e:
            print(f"An error occured from {__class__}: {e}")

    @rx.event
    def handle_create(self, form_data: dict):
        try:
            re.post(
                SettingState._url + "todos",
                headers={"Token": get_token()},
                json=form_data,
            )

        except Exception as e:
            print(f"An error occured from {__class__}: {e}")

    def delete_task(self, id):
        try:
            re.delete(
                SettingState._url + f"todos/{id}",
                headers={"Token": get_token()}
            )

        except Exception as e:
            print(f"An error occured from {__class__}: {e}")
