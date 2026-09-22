from sqlalchemy import String, ForeignKey

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(250))
    # Покажет список задач конкретного пользователя
    tasks: Mapped[list["Task"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(default="pending")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE")) # Соединение с "user.id"
    # Покажет пользователя конкретной задачи
    owner: Mapped["User"] = relationship(back_populates="tasks")
