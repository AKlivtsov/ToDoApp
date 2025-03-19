import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
    app_name="client",
    TODOAPP_SERVER_HOST=os.getenv("TODOAPP_SERVER_HOST"),
    TODOAPP_SERVER_PORT=os.getenv("TODOAPP_SERVER_PORT"),
)
