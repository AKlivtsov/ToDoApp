import reflex as rx

from webClient.states import UserState

def page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.form(
                rx.vstack(
                rx.input(
                    placeholder="Email",
                    name="email",
                ),
                rx.input(
                    placeholder="Password",
                    name="password",
                    type="password"
                ),
                rx.button("Log in", type="submit", on_click=rx.redirect("/todo")),
                rx.link("Register", href="/")
                
            ),
            on_submit=UserState.handle_login,
            reset_on_submit=True,
            )
        )
    )
