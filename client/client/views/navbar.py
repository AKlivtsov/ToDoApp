import reflex as rx

def navbar():
    return rx.flex(
        rx.badge(
            rx.icon(tag="list", size=28),
            rx.heading("ToDoApp", size="6"),
            color_scheme="green",
            radius="large",
            align="center",
            variant="surface",
            padding="0.65rem",
        ),
        rx.spacer(),
        rx.color_mode.button(),

        spacing="2",
        flex_direction="row",
        align="center",
        width="100%",
        top="0px",
        padding="1em"
    )