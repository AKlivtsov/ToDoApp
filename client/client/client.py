"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .state import State
from .views.navbar import navbar
from .views.taskItem import task_item
from .views.login import login_default
from .views.reg import signup_default


@rx.page(route="/")
def index() -> rx.Component:
    return rx.vstack(
        navbar(),

        rx.vstack(
            rx.foreach(
                State.tasks,
                lambda task: task_item(
                    title=task[0],
                    desc=task[1],
                    id_=task[2],
                    )
            ),
            width="100%",
            align="center",
        ),
    )

@rx.page(route="/login")
def login() -> rx.Component:
    return rx.vstack(
        login_default()
        )

@rx.page(route="/sign-up")
def login() -> rx.Component:
    return rx.vstack(
        signup_default()
        )

app = rx.App()
