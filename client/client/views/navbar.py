import reflex as rx
from reflex.style import toggle_color_mode

from .addTask import task_dialog
from client.state import State


def navbar():
    return rx.flex(
        actions_menu(),
        rx.spacer(),
        rx.spinner(size="2", loading=State.is_loading),
        rx.spacer(),
        task_dialog(),
        user_menu(),
        spacing="2",
        flex_direction="row",
        align="center",
        width="100%",
        top="0px",
        padding="1em",
    )


def actions_menu() -> rx.Component:
    return rx.menu.root(
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
            rx.menu.item(
                rx.icon(tag="notebook"),
                "My tasks",
                color_scheme="blue",
                on_click=rx.redirect("/"),
            ),
            rx.menu.separator(),
            rx.menu.item(
                rx.icon(tag="users"),
                "Friends",
                color_scheme="green",
                on_click=rx.redirect("/friends"),
            ),
            rx.menu.separator(),
            rx.menu.item(
                rx.icon(tag="log-out"),
                "Log out",
                color_scheme="red",
                on_click=State.log_out,
            ),
            variant="solid",
        ),
    )


def user_menu() -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.icon(tag="user", size=18),
                color_scheme="indigo",
                radius="large",
                align="center",
                variant="surface",
                padding="0.65rem",
            ),
        ),
        rx.menu.content(
            rx.menu.item(
                rx.icon(tag="user", size=18),
                "Profile setting",
                on_click=rx.redirect("/profile"),
                color_scheme="green",
                radius="large",
                align="center",
                variant="surface",
                padding="0.65rem",
            ),
            rx.menu.separator(),
            rx.menu.item(
                rx.color_mode_cond(
                    light=rx.icon("moon", size=18), dark=rx.icon("sun", size=18)
                ),
                "Change theme",
                on_click=toggle_color_mode,
                color_scheme="indigo",
                radius="large",
                align="center",
                variant="surface",
                padding="0.65rem",
            ),
        ),
    )
