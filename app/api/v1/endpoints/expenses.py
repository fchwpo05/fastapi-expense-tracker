from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from fastapi import Query

from app.db.session import get_db
from app.db.models.expense import Expense
from app.schemas import ExpenseCreate,ExpenseUpdate,ExpenseResponse
from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.schemas.expense import ExpenseCategory


router = APIRouter()


@router.post("/expenses",response_model=ExpenseResponse,status_code=status.HTTP_201_CREATED)
def create_expense(expense_in: ExpenseCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = Expense(**expense_in.model_dump(),user_id=current_user.id)
    
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("/expenses",response_model=List[ExpenseResponse])
def list_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),

    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    category: ExpenseCategory | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    sort: str = Query("desc", regex="^(asc|desc)$"),
):
    query = db.query(Expense).filter(
        Expense.user_id == current_user.id
    )

    if category:
        query = query.filter(Expense.category == category)

    if start_date:
        query = query.filter(Expense.created_at >= start_date)

    if end_date:
        query = query.filter(Expense.created_at <= end_date)

    if sort == "asc":
        query = query.order_by(Expense.created_at.asc())
    else:
        query = query.order_by(Expense.created_at.desc())

    return query.offset(offset).limit(limit).all()


@router.get("/expenses/{expense_id}",response_model=ExpenseResponse,)
def get_expense(expense_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = (db.query(Expense).filter(Expense.id == expense_id,Expense.user_id == current_user.id).first())

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    return expense


@router.put("/expenses/{expense_id}",response_model=ExpenseResponse)
def update_expense(expense_id: int,expense_in: ExpenseUpdate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = (db.query(Expense).filter(Expense.id == expense_id,Expense.user_id == current_user.id).first())

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    for field, value in expense_in.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/expenses/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = (db.query(Expense).filter(Expense.id == expense_id,Expense.user_id == current_user.id).first())

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    db.delete(expense)
    db.commit()
    return None
