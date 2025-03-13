import reflex as rx

def navbar():
    return rx.flex(
        rx.button(
            # add side bar with friends and all that stuff
            rx.icon(tag="list", size=18),
            rx.heading("ToDoApp", size="5"),
            color_scheme="green",
            radius="large",
            align="center",
            variant="surface",
            padding="0.65rem",

            on_click=rx.redirect("/sign-in"), # remove that when sidebar ready
        ),
        rx.spacer(),
        rx.button(
            rx.icon(tag="plus", size=18),
            rx.heading("Add task", size='3'),
            color_scheme='indigo',
            radius="large",
            align="center",
            variant="surface",
            padding="0.65rem",
        ),
        rx.button(
            rx.icon(tag="rotate-cw", size=18),
            color_scheme='indigo',
            radius="large",
            align="center",
            variant="surface",
            padding="0.65rem",
        ),
        rx.color_mode.button(
            color_scheme='indigo',
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
        padding="1em"
    )