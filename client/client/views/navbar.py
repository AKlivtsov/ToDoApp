import reflex as rx

from .addTask import task_dialog
from client.state import State


def navbar():
    return rx.flex(
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon(tag="list", size=18),
                    rx.heading("ToDoApp", size="5"),
                    color_scheme="green",
                    radius="large",
                    align="center",
                    variant="surface",
                    padding="0.65rem",
                ),
            ),
            rx.menu.content(
                rx.menu.item(rx.icon(tag="users"), "Friends", disabled=True),
                rx.menu.separator(),
                rx.menu.item(
                    rx.icon(tag="log-out"),
                    "Log out",
                    color_scheme="red",
                    on_click=State.log_out,
                ),
                variant="solid",
            ),
        ),
        rx.spacer(),
        rx.spinner(size="2", loading=State.is_loading),
        rx.spacer(),
        task_dialog(),
        rx.color_mode.button(
            color_scheme="indigo",
            radius="large",
            align="center",
            variant="surface",
            padding="0.65rem",
        ),
        spacing="2",
        flex_direction="row",
        align="center",
        width="100%",
        top="0px",
        padding="1em",
    )
