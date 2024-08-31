import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User

pytestmark = pytest.mark.asyncio

async def test_create_user(async_session: AsyncSession):
    new_user = User(
        github_id=12345,
        login="testuser",
        name="Test User",
        email="testuser@example.com",
        avatar_url="https://example.com/avatar.jpg"
    )
    async_session.add(new_user)
    await async_session.commit()

    result = await async_session.execute(select(User).where(User.login == "testuser"))
    user = result.scalars().first()

    assert user is not None
    assert user.github_id == 12345
    assert user.login == "testuser"
    assert user.name == "Test User"
    assert user.email == "testuser@example.com"
    assert user.avatar_url == "https://example.com/avatar.jpg"
    assert user.created_at is not None

async def test_update_user(async_session: AsyncSession):
    new_user = User(
        github_id=67890,
        login="updateuser",
        name="Update User",
        email="updateuser@example.com"
    )
    async_session.add(new_user)
    await async_session.commit()

    result = await async_session.execute(select(User).where(User.login == "updateuser"))
    user = result.scalars().first()
    user.name = "Updated Name"
    user.email = "newemail@example.com"
    await async_session.commit()

    result = await async_session.execute(select(User).where(User.login == "updateuser"))
    updated_user = result.scalars().first()

    assert updated_user is not None
    assert updated_user.name == "Updated Name"
    assert updated_user.email == "newemail@example.com"

async def test_delete_user(async_session: AsyncSession):
    new_user = User(
        github_id=13579,
        login="deleteuser",
        name="Delete User",
        email="deleteuser@example.com"
    )
    async_session.add(new_user)
    await async_session.commit()

    result = await async_session.execute(select(User).where(User.login == "deleteuser"))
    user = result.scalars().first()
    await async_session.delete(user)
    await async_session.commit()

    result = await async_session.execute(select(User).where(User.login == "deleteuser"))
    deleted_user = result.scalars().first()

    assert deleted_user is None