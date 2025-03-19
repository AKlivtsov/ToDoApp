import reflex as rx

from client.state import State

def goto_login() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Sorry, it's seems to be that you're not authentificated. Please, proceed to the login or register page.",
            align="center",
            ),
        rx.hstack(
            rx.spacer(),
            rx.button(
                "Login",
                color_scheme='indigo',
                radius="large",
                align="center",
                variant="surface",
                padding="0.65rem",
                on_click=rx.redirect("/sign-in")
            ),
            rx.button(
                "Register",
                color_scheme='indigo',
                radius="large",
                align="center",
                variant="surface",
                padding="0.65rem",
                on_click=rx.redirect("/sign-up")
            ),
            rx.spacer(),
            width="100%"
        ),
        width="100%",
        padding="4em",
        spacing="4"
    )
