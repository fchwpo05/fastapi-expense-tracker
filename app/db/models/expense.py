from __future__ import annotations
from sqlalchemy import String, Float, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING

from app.db.base import Base
if TYPE_CHECKING:
    from app.db.models.user import User

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="expenses"
    )

    __table_args__ = (
        Index("idx_expenses_user_id", "user_id"),
        Index("idx_expenses_created_at", "created_at"),
        Index("idx_expenses_user_created", "user_id", "created_at"),
    )



