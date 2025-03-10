"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .views.navbar import navbar


class State(rx.State):
    tasks : list[list[str]] = [
        ["Task1", "deesc 1", "1"],
        ["Task1", "deesc 1", "2"],
        ["Task3", "deesc 1", "3"],
        ["Task89", "deesc 1", "4"],
    ]

def task_item(title: str, desc: str, id_:str) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.heading(title),
                rx.text(desc),
                ),
            rx.spacer(),
            rx.button(
                rx.icon("pencil"),
            ),
        ),
        width="90%",
    )

def index() -> rx.Component:
    return rx.vstack(
        navbar(),

        rx.vstack(
            rx.foreach(
                State.tasks,
                lambda task: task_item(
                    title=task[0],
                    desc=task[1],
                    id_=task[2]
                    )
            ),
            width="100%",
            align="center",
        ),
    )

app = rx.App()
app.add_page(index)
