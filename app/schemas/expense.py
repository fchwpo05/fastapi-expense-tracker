from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ExpenseBase(BaseModel):
    title: str
    amount: float
    category: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }