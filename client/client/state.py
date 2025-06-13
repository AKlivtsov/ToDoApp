import reflex as rx
import httpx
from rxconfig import config


class State(rx.State):
    is_loading: bool
    _base_url: str = f"{config.TODOAPP_SERVER_HOST}:{config.TODOAPP_SERVER_PORT}"
    token: str
    tasks: list[dict[str, str]]

    @rx.event
    def log_out(self):
        self.token = ""

    @rx.event
    async def update_tasks(self):
        self.is_loading = True
        headers = {"Authorization": self.token}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._base_url + "/api/todos?Limit=99&Page=1", headers=headers
            )
            self.tasks = response.json()["data"]
            self.is_loading = False

    @rx.event
    async def delete_task(self, id_: str):
        self.is_loading = True
        headers = {"Authorization": self.token}
        async with httpx.AsyncClient() as client:
            await client.delete(self._base_url + f"/api/todos/{id_}", headers=headers)
            await self.update_tasks()
            return rx.toast("Task deleted.")

    @rx.event
    async def handle_reg(self, user_data: dict):
        self.is_loading = True
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._base_url + "/auth/sign-up", json=user_data
            )

            try:
                self.token = response.json()["token"]
                await self.update_tasks()

            except KeyError or json.decoder.JSONDecodeError:
                self.token = ""

    @rx.event
    async def handle_login(self, user_data: dict):
        self.is_loading = True
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._base_url + "/auth/sign-in", json=user_data
            )

            try:
                self.token = response.json()["token"]
                await self.update_tasks()

            except KeyError or json.decoder.JSONDecodeError:
                self.token = ""

    @rx.event
    async def create_task(self, task_data: dict):
        headers = {"Authorization": self.token}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._base_url + "/api/todos", json=task_data, headers=headers
            )

            if response.status_code == 200:
                await self.update_tasks()
                yield rx.toast("Task created.")
            else:
                yield rx.toast(
                    f"Unknown error. Server have been returned code {response.status_code}"
                )

    @rx.event
    async def edit_task(self, task_data: dict):
        self.is_loading = True
        headers = {"Authorization": self.token}
        async with httpx.AsyncClient() as client:
            response = await client.put(
                self._base_url + "/api/todos/" + task_data["id"],
                json=task_data,
                headers=headers,
            )

            if response.status_code == 200:
                await self.update_tasks()
                return rx.toast("Task updated.")
            else:
                return rx.toast(
                    f"Unknown error. Server have been returned code {response.status_code}"
                )
