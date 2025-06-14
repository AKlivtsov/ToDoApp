import reflex as rx

from client.state import State
from .editTask import edit_dialog


def task_item(task: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.heading(task["title"]),
                rx.text(task["description"]),
            ),
            rx.spacer(),
            rx.vstack(
                rx.spacer(),
                rx.vstack(
                    edit_dialog(task),
                    rx.button(
                        rx.icon("trash", size=20),
                        color_scheme="ruby",
                        radius="large",
                        align="center",
                        variant="surface",
                        padding="0.65rem",
                        on_click=State.delete_task(task["id"]),
                    ),
                ),
                spacing="2",
            ),
        ),
        width="90%",
    )
