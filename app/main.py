from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base

from app.routes import auth_router
from app.routes import products_router
from app.routes import categories_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Product API",
    description="API de gestion de produits avec authentification JWT",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)
app.include_router(auth_router)
app.include_router(products_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
