
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from expenses.routes import router as expenses_routes
from users.routes import router as users_routes
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
import time


tags_metadata = [
    {
        "name": "expenses",
        "description": "Operations related to expense tracking and management",
        "externalDocs": {
            "description": "More about expense management",
            "url": "https://github.com/AliGanji14"
        }
    }
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    Base.metadata.create_all(bind=engine)
    yield
    print("Application shutdown")

app = FastAPI(docs_url="/docs",
              title="Expense Management Application",
              description="This section handles expense tracking and management",
              version="0.0.1",
              contact={
                      "name": "Ali Ganji",
                      "url": "https://github.com/AliGanji14",
                      "email": "aliganji1309@gmail.com",
              },
              license_info={
                  "name": "MIT",
              },
              lifespan=lifespan,
              openapi_tags=tags_metadata)


app.include_router(users_routes)
app.include_router(expenses_routes)


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
