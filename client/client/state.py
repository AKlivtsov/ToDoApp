import reflex as rx

import httpx

class State(rx.State):
    is_loading: bool
    _base_url: str = "http://localhost:8080"
    token :str
    tasks: list[dict[str, str]] = [{
                "title": "please, login or register",
                "description": "go to /sign-in or /sign-up",
                "id": "0"
                }]

    @rx.event
    async def update_tasks(self):
        self.is_loading = True
        headers= {"Authorization": self.token}
        async with httpx.AsyncClient() as client:
            response = await client.get(self._base_url + "/api/todos?Limit=99&Page=1", headers=headers)
            self.tasks = response.json()['data']
            self.is_loading = False

    @rx.event
    async def delete_task(self, id_: str):
        self.is_loading = True
        headers= {"Authorization": self.token}
        async with httpx.AsyncClient() as client:
            await client.delete(self._base_url + f"/api/todos/{id_}", headers=headers)
            await self.update_tasks()
                
    @rx.event
    async def handle_reg(self, user_data: dict):
        self.is_loading = True
        print(user_data)
        async with httpx.AsyncClient() as client:
            response = await client.post(self._base_url + "/auth/sign-up", json=user_data)

            try:
                self.token = response.json()['token']
                await self.update_tasks()

            except KeyError:
                self.token = ""

    @rx.event
    async def handle_login(self, user_data: dict):
        self.is_loading = True
        async with httpx.AsyncClient() as client:
            response = await client.post(self._base_url + "/auth/sign-in", json=user_data)

            try:
                self.token = response.json()['token']
                await self.update_tasks()

            except KeyError:
                self.token = ""

    @rx.event
    async def create_task(self, task_data: dict):
        headers= {"Authorization": self.token}
        async with httpx.AsyncClient() as client:
            response = await client.post(self._base_url + "/api/todos", json=task_data, headers=headers)

            if response.status_code == 200:
                await self.update_tasks()
            # make error pop-up 

    @rx.event
    async def edit_task(self, task_data: dict):
        self.is_loading = True
        headers= {"Authorization": self.token}
        async with httpx.AsyncClient() as client:
            response = await client.put(self._base_url + "/api/todos/"+ task_data["id"], json=task_data, headers=headers)

            if response.status_code == 200:
                await self.update_tasks()
