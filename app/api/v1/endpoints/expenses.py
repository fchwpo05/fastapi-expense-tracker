from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.db.models.expense import Expense
from app.schemas import ExpenseCreate,ExpenseUpdate,ExpenseResponse
from app.core.dependencies import get_current_user
from app.db.models.user import User


router = APIRouter()


@router.post("/expenses",response_model=ExpenseResponse,status_code=status.HTTP_201_CREATED)
def create_expense(expense_in: ExpenseCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = Expense(**expense_in.model_dump(),user_id=current_user.id)
    
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("/expenses",response_model=List[ExpenseResponse])
def list_expenses(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return (db.query(Expense).filter(Expense.user_id == current_user.id).order_by(Expense.created_at.desc()).all())


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

    for field, value in expense_in.model_dump().items():
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
