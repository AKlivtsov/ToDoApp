import reflex as rx 

from client.state import State

def task_item(title: str, desc: str, id_:str) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.heading(title),
                rx.text(desc),
                ),
            rx.spacer(),
            rx.vstack(
                rx.button(
                    rx.icon("pencil", size=20),
                    color_scheme='indigo',
                    radius="large",
                    align="center",
                    variant="surface",
                    padding="0.65rem",
                ),
                rx.button(
                    rx.icon("trash", size=20),
                    color_scheme='ruby',
                    radius="large",
                    align="center",
                    variant="surface",
                    padding="0.65rem",
                    on_click=State.delete_task(id_)
                ),
                spacing="2",
            ),
        ),
        width="90%",
    )
