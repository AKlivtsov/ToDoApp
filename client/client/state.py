import reflex as rx

import requests as req

class State(rx.State):
    _base_url: str = "http://localhost:8080"
    token :str = "dced2ee9-df91-4d39-8f81-636e704d9465"

    @rx.var
    def tasks(self) -> list[list[str]]:
        headers= {"Authorization": self.token}
        response = req.get(self._base_url + "/api/todos?Limit=99&Page=1", headers=headers)

        task_list = []
        for task in response.json()['data']:
            task_list.append([task['title'], task['description'], task['id']])

        return task_list
    
    def delete_task(self, id_: str) -> None:
        headers= {"Authorization": self.token}
        req.delete(self._base_url + "/api/todos/" + str(id_), headers=headers)
        