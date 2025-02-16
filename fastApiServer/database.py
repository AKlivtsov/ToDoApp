import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, ForeignKey, inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import database_exists, create_database

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))


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
