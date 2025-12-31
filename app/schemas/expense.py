from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum

class ExpenseCategory(str, Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    RENT = "Rent"
    UTILITIES = "Utilities"
    SHOPPING = "Shopping"
    OTHER = "Other"


class ExpenseBase(BaseModel):
    title: str
    amount: float
    category: ExpenseCategory = ExpenseCategory.OTHER

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v

class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    title: str | None = None
    amount: float | None = None
    category: ExpenseCategory | None = None


class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }