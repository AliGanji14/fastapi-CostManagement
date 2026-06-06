from collections.abc import Callable
from fastapi import APIRouter, status, Query, HTTPException, Path, Depends
from typing import List
from sqlalchemy.orm import Session
from expenses.schemas import (
    ExpenseResponseSchema,
    ExpenseCreateSchema,
    ExpenseUpdateSchema,
)
from core.database import get_db
from expenses.models import Expense
from users.models import UserModel
from auth.jwt_auth import get_authenticate_user
from core.i18n import get_translator

router = APIRouter(tags=["expenses"])


@router.get(
    "/expenses",
    status_code=status.HTTP_200_OK,
    response_model=List[ExpenseResponseSchema],
)
def get_expenses(
    q: str | None = Query(
        description="Search expenses by description",
        example="Internet",
        alias="search",
        max_length=50,
        default=None,
    ),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticate_user),
):
    query = db.query(Expense).filter_by(user_id=user.id)
    if q:
        query = query.filter_by(description=q)
    results = query.all()
    return results


@router.post(
    "/expenses",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseResponseSchema,
)
def create_expense(
    request: ExpenseCreateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticate_user),
):
    data = request.model_dump()
    data.update({"user_id": user.id})
    expenses_obj = Expense(**data)
    db.add(expenses_obj)
    db.commit()
    db.refresh(expenses_obj)
    return expenses_obj


@router.get(
    "/expenses/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponseSchema,
)
def get_expense(
    expense_id: int = Path(description="The ID of the cost in expenses"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticate_user),
    _: Callable[[str], str] = Depends(get_translator),
):
    expense_obj = db.query(Expense).filter_by(user_id=user.id, id=expense_id).first()
    if not expense_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=_("cost not found")
        )
    return expense_obj


@router.put(
    "/expenses/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponseSchema,
)
def update_expense(
    request: ExpenseUpdateSchema,
    expense_id: int = Path(description="The ID of the cost in expenses"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticate_user),
    _: Callable[[str], str] = Depends(get_translator),
):
    expense_obj = db.query(Expense).filter_by(user_id=user.id, id=expense_id).first()
    if not expense_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=_("cost not found")
        )
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(expense_obj, field, value)

    db.commit()
    db.refresh(expense_obj)
    return expense_obj


@router.delete("/expenses/{expense_id}", status_code=status.HTTP_200_OK)
def delete_expense(
    expense_id: int = Path(description="The ID of the cost in expenses"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticate_user),
    _: Callable[[str], str] = Depends(get_translator),
):
    expense_obj = db.query(Expense).filter_by(user_id=user.id, id=expense_id).first()
    if not expense_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=_("cost not found")
        )
    db.delete(expense_obj)
    db.commit()
