import reflex as rx

from client.state import State


def friends_view() -> rx.Component:
    return rx.vstack(friends_search(), width="90%")


def friends_search() -> rx.Component:
    return rx.form(
        rx.card(
            rx.hstack(
                rx.heading("Add friend!"),
                rx.spacer(),
                rx.input(placeholder="Enter friend's email", name="email"),
                rx.button(
                    rx.icon("search", size=18),
                    color_scheme="indigo",
                    radius="large",
                    align="center",
                    variant="surface",
                    padding="0.65rem",
                    type="submit",
                ),
            ),
            rx.vstack(
                rx.foreach(State.found_friends, lambda data: friends_found_item(data))
            ),
            width="100%",
            radius="large",
        ),
        reset_on_submit=True,
        on_submit=State.handle_friend_search,
    )


def friends_found_item(data) -> rx.Component:
    return rx.card()
