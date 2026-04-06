from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.db.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


def create_expense(db: Session, user_id: int, data: ExpenseCreate):
    expense = Expense(**data.model_dump(), user_id=user_id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses(
    db: Session,
    user_id: int,
    limit: int,
    offset: int,
    category: str | None,
    start_date: date | None,
    end_date: date | None,
    sort: str,
):
    query = db.query(Expense).filter(Expense.user_id == user_id)

    if category:
        query = query.filter(Expense.category == category)

    if start_date:
        query = query.filter(Expense.created_at >= start_date)

    if end_date:
        query = query.filter(Expense.created_at <= end_date)

    total = db.query(func.count(Expense.id)).filter(
        Expense.user_id == user_id
    ).scalar()

    if sort == "asc":
        query = query.order_by(Expense.created_at.asc())
    else:
        query = query.order_by(Expense.created_at.desc())

    items = query.offset(offset).limit(limit).all()

    next_offset = offset + limit if offset + limit < total else None

    return items, total, next_offset


def get_expense(db: Session, user_id: int, expense_id: int):
    return db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user_id
    ).first()


def update_expense(db: Session, expense: Expense, data: ExpenseUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense: Expense):
    db.delete(expense)
    db.commit()