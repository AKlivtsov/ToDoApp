import reflex as rx

from rxconfig import config
from .state import State
from .views.navbar import navbar
from .views.taskItem import task_item
from .views.login import login_default
from .views.reg import signup_default
from .views.redirect import goto_login
from .views.friends_list import friends_view
from .views.profile import profile_setting


@rx.page(route="/")
def index() -> rx.Component:
    return rx.cond(
        State.token,
        rx.vstack(
            navbar(),
            rx.vstack(
                rx.foreach(State.tasks, task_item),
                width="100%",
                align="center",
            ),
        ),
        goto_login(),
    )


@rx.page(route="/sign-in")
def login() -> rx.Component:
    return rx.vstack(
        rx.spacer(),
        login_default(),
        width="100%",
        align="center",
    )


@rx.page(route="/sign-up")
def reg() -> rx.Component:
    return rx.vstack(
        rx.spacer(),
        signup_default(),
        width="100%",
        align="center",
    )


@rx.page(route="/friends")
def friends() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.vstack(
            friends_view(),
            width="100%",
            align="center",
        ),
    )

@rx.page(route="/profile")
def profile() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.vstack(
            profile_setting(),
            width="100%",
            align="center",
        )
    )

app = rx.App()
