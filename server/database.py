import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped, relationship

load_dotenv()
engine = create_engine(os.getenv("DATABASE"))


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    task: Mapped[list["Task"]] = relationship(back_populates="user", uselist=True, lazy='joined')


class Task(Base):
    __tablename__ = 'tasks'

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    user: Mapped["User"] = relationship(back_populates="task", uselist=False)
    user_fk = mapped_column(ForeignKey('users.id'))

# Base.metadata.create_all(engine)
