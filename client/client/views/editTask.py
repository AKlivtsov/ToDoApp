import reflex as rx 

from client.state import State

def edit_dialog(task: dict) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("pencil", size=20),
                color_scheme='indigo',
                radius="large",
                align="center",
                variant="surface",
                padding="0.65rem",
            ),
        ),
        rx.dialog.content(
            rx.form(
                rx.vstack(
                    rx.hstack(
                        rx.dialog.title("Task"),
                        rx.input(
                            value=task["id"],
                            read_only=True,
                            width="40px",
                            size="1",
                            name="id",
                            ),
                        rx.text("is being edited!")
                    ),
                    rx.vstack(
                        rx.text(
                            "Title",
                            size="3",
                            weight="medium",
                            text_align="left",
                            width="100%",
                        ),
                        rx.input(
                            placeholder=task["title"],
                            size="3",
                            width="100%",
                            name="title",
                        ),
                        justify="start",
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(
                            "Description",
                            size="3",
                            weight="medium",
                            text_align="left",
                            width="100%",
                        ),
                        rx.input(
                            placeholder=task["description"],
                            size="3",
                            width="100%",
                            name="description",
                        ),
                        justify="start",
                        spacing="2",
                        width="100%",
                    ),
                    rx.hstack(
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            "Save and exit",
                            color_scheme='indigo',
                            radius="large",
                            align="center",
                            variant="surface",
                            padding="0.65rem",
                            size="3", 
                            type="submit",
                            ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Exit without saving",
                            color_scheme='ruby',
                            radius="large",
                            align="center",
                            variant="surface",
                            padding="0.65rem",
                            size="3",
                            ),
                    ),
                    width="100%"
                ),
                    spacing="4",
                ),
                on_submit=State.edit_task,
                reset_on_submit=True,
            ),
        )
    )