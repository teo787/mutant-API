import pytest
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv(".env.test")

from main import app
from db.db import get_session
from httpx import AsyncClient
from core.cache import get_cache
from core.rate_limit import limiter
import pytest_asyncio
import os

os.environ["ENV"]="test"

TEST_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest_asyncio.fixture
def session():
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest_asyncio.fixture(autouse=True)
def override_db(session):
    app.dependency_overrides[get_session] = lambda: session
    yield
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

class FakeCache:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ttl=300):
        self.store[key] = value

    async def delete(self, key):
        self.store.pop(key, None)


@pytest_asyncio.fixture(autouse=True)
def override_cache():
    app.dependency_overrides[get_cache] = lambda: FakeCache()
    yield
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(autouse=True)
def disable_rate_limit():
    limiter.enabled = False
    yield
    limiter.enabled = True