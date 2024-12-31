import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped

load_dotenv()
engine = create_engine('sqlite+pysqlite:///webClient/database/database.db')

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    token: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
