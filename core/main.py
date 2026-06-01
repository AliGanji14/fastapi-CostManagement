from fastapi import FastAPI, status, Query, HTTPException, Path, Depends
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Response, Request
from contextlib import asynccontextmanager
from typing import List
from sqlalchemy.orm import Session
from users.routes import router as users_routes
from fastapi.middleware.cors import CORSMiddleware
from schemas import ExpenseCreateSchema, ExpenseResponseSchema, ExpenseUpdateSchema
from database import Base, engine, get_db, Expense
from auth.jwt_auth import get_authenticate_user
import time
from users.models import UserModel


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Application startup')
    Base.metadata.create_all(engine)
    yield
    print('Application shutdown')

app = FastAPI(lifespan=lifespan)

app.include_router(users_routes)


@app.get('/expenses', status_code=status.HTTP_200_OK, response_model=List[ExpenseResponseSchema])
def get_expenses(q: str | None = Query(
        description='Search expenses by description',
        example='Internet',
        alias='search',
        max_length=50,
        default=None),
        db: Session = Depends(get_db),
        user: UserModel = Depends(get_authenticate_user)):
    query = db.query(Expense).filter_by(user_id=user.id)
    if q:
        query = query.filter_by(description=q)
    results = query.all()
    return results


@app.post('/expenses', status_code=status.HTTP_201_CREATED, response_model=ExpenseResponseSchema)
def create_expense(request: ExpenseCreateSchema, db: Session = Depends(get_db), user: UserModel = Depends(get_authenticate_user)):
    data = request.model_dump()
    data.update({'user_id': user.id})
    expenses_obj = Expense(**data)
    db.add(expenses_obj)
    db.commit()
    db.refresh(expenses_obj)
    return expenses_obj


@app.get('/expenses/{expense_id}', status_code=status.HTTP_200_OK, response_model=ExpenseResponseSchema)
def get_expense(expense_id: int = Path(description='The ID of the cost in expenses'), db: Session = Depends(get_db), user: UserModel = Depends(get_authenticate_user)):
    expense_obj = db.query(Expense).filter_by(
        user_id=user.id, id=expense_id).first()
    if not expense_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='cost not found')
    return expense_obj


@app.put('/expenses/{expense_id}', status_code=status.HTTP_200_OK, response_model=ExpenseResponseSchema)
def update_expense(request: ExpenseUpdateSchema, expense_id: int = Path(description='The ID of the cost in expenses'), db: Session = Depends(get_db), user: UserModel = Depends(get_authenticate_user)):
    expense_obj = db.query(Expense).filter_by(
        user_id=user.id, id=expense_id).first()
    if not expense_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='cost not found')
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(expense_obj, field, value)

    db.commit()
    db.refresh(expense_obj)
    return expense_obj


@app.delete('/expenses/{expense_id}', status_code=status.HTTP_200_OK)
def delete_expense(expense_id: int = Path(description='The ID of the cost in expenses'), db: Session = Depends(get_db), user: UserModel = Depends(get_authenticate_user)):
    expense_obj = db.query(Expense).filter_by(
        user_id=user.id, id=expense_id).first()
    if not expense_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='cost not found')
    db.delete(expense_obj)
    db.commit()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
