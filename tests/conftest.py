import os

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.models import Base  # ou depuis app.models.base si séparé
from app.database import get_db  # le remplacer pour les tests

os.environ["ENV_FILE"] = ".env.test"
from app.settings import settings

engine_test = create_async_engine(settings.database_url, echo=False)
TestingSessionLocal = async_sessionmaker(bind=engine_test, expire_on_commit=False)

# Remplacement de la dépendance get_db
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Création des tables avant les tests
@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# Client HTTP de test
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture(autouse=True)
async def clear_db():
    async with engine_test.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
