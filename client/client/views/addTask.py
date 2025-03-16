import reflex as rx 

from client.state import State

def task_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon(tag="plus", size=18),
                rx.heading("Add task", size='3'),
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
                    rx.dialog.title(
                        "Add task here!"
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
                            placeholder="Buy bread.",
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
                            placeholder="And a lot of milk!!!",
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
                on_submit=State.create_task,
                reset_on_submit=True,
            ),
        )
    )