import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, ForeignKey, inspect, URL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import database_exists, create_database

load_dotenv()
DB_URL = URL.create(
    "postgresql",
    username=os.getenv("POSTGRES_USERNAME"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
)
engine = create_engine(DB_URL)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    task: Mapped[list["Task"]] = relationship(back_populates="user", uselist=True, lazy='joined')


class Task(Base):
    __tablename__ = 'tasks'

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    user: Mapped["User"] = relationship(back_populates="task", uselist=False)
    user_fk = mapped_column(ForeignKey('users.id'))


# Check if tables exist and create if not
inspector = inspect(engine)
if not inspector.get_table_names():
    Base.metadata.create_all(engine)
