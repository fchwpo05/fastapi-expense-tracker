from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from fastapi import Query

from app.db.session import get_db
from app.db.models.expense import Expense
from app.schemas import ExpenseCreate,ExpenseUpdate,ExpenseResponse,ExpenseListResponse
from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.schemas.expense import ExpenseCategory
from app.services import expense_service


router = APIRouter()


@router.post("/expenses",response_model=ExpenseResponse,status_code=status.HTTP_201_CREATED)
def create_expense(expense_in: ExpenseCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return expense_service.create_expense(
        db=db,
        user_id=current_user.id,
        data=expense_in,
    )


@router.get("/expenses",response_model=ExpenseListResponse)
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
    items, total, next_offset = expense_service.get_expenses(
        db=db,
        user_id=current_user.id,
        limit=limit,
        offset=offset,
        category=category,
        start_date=start_date,
        end_date=end_date,
        sort=sort,
    )

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "next_offset": next_offset,
    }


@router.get("/expenses/{expense_id}",response_model=ExpenseResponse,)
def get_expense(expense_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = expense_service.get_expense(
        db=db,
        user_id=current_user.id,
        expense_id=expense_id,
    )

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    return expense


@router.put("/expenses/{expense_id}",response_model=ExpenseResponse)
def update_expense(expense_id: int,expense_in: ExpenseUpdate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = expense_service.get_expense(
        db=db,
        user_id=current_user.id,
        expense_id=expense_id,
    )

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    return expense_service.update_expense(
        db=db,
        expense=expense,
        data=expense_in,
    )


@router.delete("/expenses/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = expense_service.get_expense(
        db=db,
        user_id=current_user.id,
        expense_id=expense_id,
    )

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    expense_service.delete_expense(db=db, expense=expense)
    return None
