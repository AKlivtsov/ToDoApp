import reflex as rx

from webClient.states import UserState


def page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.form(
                rx.vstack(
                rx.input(
                    placeholder="Username",
                    name="name",
                ),
                rx.input(
                    placeholder="Email",
                    name="email",
                ),
                rx.input(
                    placeholder="Password",
                    name="password",
                    type="password"
                ),
                rx.button("Register", type="submit", on_click=rx.redirect("/todo")),
                rx.link("Sign in", href="/login")
                
            ),
            on_submit=UserState.handle_registration,
            reset_on_submit=True,
            )
        )
    )
