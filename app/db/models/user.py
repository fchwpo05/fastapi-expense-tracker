from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.db.base import Base
if TYPE_CHECKING:
    from app.db.models.expense import Expense


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    expenses: Mapped[List["Expense"]] = relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan"
    )