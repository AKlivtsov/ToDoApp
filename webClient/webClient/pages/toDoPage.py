import reflex as rx

from webClient.states import TaskState

def create_popup() ->rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.button(
                rx.icon("plus"),
                color_scheme="green"
                ),
        ),
        rx.popover.content(
            rx.form(
                rx.input(
                    placeholder="Title",
                    name="title"
                ),
                rx.input(
                    placeholder="Description",
                    name="description"
                ),
                rx.popover.close(
                    rx.button("Create", type="submit")
                    ),
                
                on_submit=TaskState.handle_create,
                reset_on_submit=True,
            ),
        ),
    )

def edit_popup(id) -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.button(
                rx.icon("pencil-line"),
                color_scheme="blue"
                ),
        ),
        rx.popover.content(
            rx.form(
                rx.hstack(
                    rx.text("You changing task:"),
                    rx.input(
                        value=id,
                        read_only=True,
                        name="id",
                    ),
                ),
                rx.input(
                    placeholder="Title",
                    name="title"
                ),
                rx.input(
                    placeholder="Description",
                    name="description"
                ),
                rx.popover.close(
                    rx.button("Edit", type="submit")
                    ),
                
                on_submit=TaskState.handle_edit,
                reset_on_submit=True,
            ),
        ),
    )

def task_item(task_data: dict) -> rx.Component:
    return rx.card(

        rx.hstack(
            rx.vstack(
                rx.heading(task_data["title"]),
                rx.text(task_data["description"]),
                ),
            rx.vstack(
                rx.button(
                    rx.icon("trash-2"),
                    color_scheme="ruby",
                    on_click=TaskState.delete_task(task_data["id"])),
                edit_popup(task_data["id"]),
                )
        )
        
    )

def page() -> rx.Component:
    return rx.center(
        rx.vstack(
            create_popup(),
            rx.foreach(TaskState.tasks, task_item),
            align="center"
        )
    )
