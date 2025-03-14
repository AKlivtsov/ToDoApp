import reflex as rx

from client.state import State

def signup_default() -> rx.Component:
    return rx.card(
        rx.form(
        rx.vstack(
            rx.center(
                rx.badge(
                    rx.heading("ToDoApp", size="5"),
                    rx.text(
                        "ver. 1.0",
                        color_scheme='grass',
                        weight="bold"
                        ),
                    color_scheme="green",
                    radius="large",
                    align="center",
                    variant="surface",
                    padding="0.65rem",
                ),
                rx.heading(
                    "Create an account",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Username",
                    size="3",
                    weight="medium",
                    type="username",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="user",
                    type="",
                    size="3",
                    width="100%",
                    name="username",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Email address",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="user@akcloud.dev",
                    type="email",
                    size="3",
                    width="100%",
                    name="email",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Password",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="Enter your password",
                    type="password",
                    size="3",
                    width="100%",
                    name="password",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.button("Register", size="3", width="100%", type="submit", on_click=rx.redirect("/")),
            rx.center(
                rx.text("Already registered?", size="3"),
                rx.link("Sign in", href="/sign-in", size="3"),
                opacity="0.8",
                spacing="2",
                direction="row",
            ),
            spacing="6",
            width="100%",
        ),
        on_submit=State.handle_reg,
        reset_on_submit=True,
        ),
        size="4",
        max_width="28em",
        width="100%",
    )