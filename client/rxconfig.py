import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
    app_name="client",
    api_url=os.getenv("REFLEX_API_URL"),
    TODOAPP_SERVER_HOST=os.getenv("TODOAPP_SERVER_HOST"),
    TODOAPP_SERVER_PORT=os.getenv("TODOAPP_SERVER_PORT"),
)
