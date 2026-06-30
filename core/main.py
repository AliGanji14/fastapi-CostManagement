from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from expenses.routes import router as expenses_routes
from users.routes import router as users_routes
from i18n_routes import router as i18n_routes
from core.database import Base, engine
from core.exceptions import ExpenseNotFoundException
from core.config import settings
import httpx
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

tags_metadata = [
    {
        "name": "expenses",
        "description": "Operations related to expense tracking and management",
        "externalDocs": {
            "description": "More about expense management",
            "url": "https://github.com/AliGanji14",
        },
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    Base.metadata.create_all(bind=engine)
    yield
    print("Application shutdown")


app = FastAPI(
    docs_url="/docs",
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
    openapi_tags=tags_metadata,
)


app.include_router(users_routes)
app.include_router(expenses_routes)
app.include_router(i18n_routes)


@app.exception_handler(ExpenseNotFoundException)
async def expense_not_found_exception_handler(
    request: Request, exc: ExpenseNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"status": "error", "message": exc.message},
    )


redis = aioredis.from_url(settings.REDIS_URL)
cache_backend = RedisBackend(redis)
FastAPICache.init(cache_backend, prefix="fastapi-cache")


async def request_current_weather(latitude: float, longitude: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        current_weather = data.get("current", {})
        return current_weather
    else:
        return None


@app.get("/fetch-current-weather", status_code=200)
@cache(expire=10)
async def fetch_current_weather(latitude: float = 40.7128, longitude: float = -74.0060):
    current_weather = await request_current_weather(latitude, longitude)
    if current_weather:

        return JSONResponse(content={"current_weather": current_weather})
    else:
        return JSONResponse(
            content={"detail": "Failed to fetch weather"}, status_code=500
        )


@app.get("/is_ready", status_code=200)
async def readiness():
    return JSONResponse(content="ok")
