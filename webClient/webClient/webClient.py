# web stuff
import reflex as rx
from rxconfig import config

# pages
from webClient.pages.registerPage import page as redPage
from webClient.pages.toDoPage import page as toDoPage
from webClient.pages.loginPage import page as loginPage

# states
from webClient.states import UserState


@rx.page(route="/")
def register_login_page() -> rx.Component:
    return redPage()

@rx.page(route="/login")
def login_page() -> rx.Component:
    return loginPage()

@rx.page(route="/todo")
def todo_page() -> rx.Component:
    return toDoPage()


app = rx.App()
