import pytest
import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, create_tables, drop_tables
from app.core.config import settings

@pytest.fixture(scope="session")
def setup_test_environment():
    # Set the TESTING environment variable
    os.environ["TESTING"] = "1"
    yield
    # Unset the TESTING environment variable
    del os.environ["TESTING"]

@pytest.fixture(scope="session")
async def create_test_database(setup_test_environment):
    # Create tables
    await create_tables()
    yield
    # Drop tables
    await drop_tables()

@pytest.fixture(scope="function")
async def async_session(create_test_database) -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
        # Roll back the transaction after each test
        await session.rollback()