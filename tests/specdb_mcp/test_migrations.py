import pytest
import aiosqlite
from specdb_mcp.schema import ALL_CREATE_STATEMENTS
from specdb_mcp.migrations import (
    get_current_version,
    apply_migrations,
    CURRENT_VERSION,
)


@pytest.fixture
async def db():
    async with aiosqlite.connect(":memory:") as database:
        for sql in ALL_CREATE_STATEMENTS:
            await database.execute(sql)
        await database.commit()
        yield database


async def test_get_current_version_empty_db(db):
    version = await get_current_version(db)
    assert version == 0


async def test_apply_migrations_sets_version(db):
    version = await apply_migrations(db)
    assert version == CURRENT_VERSION


async def test_schema_version_row_recorded(db):
    await apply_migrations(db)
    async with db.execute("SELECT version FROM schema_version") as cursor:
        row = await cursor.fetchone()
    assert row is not None
    assert row[0] == CURRENT_VERSION


async def test_apply_migrations_idempotent(db):
    v1 = await apply_migrations(db)
    v2 = await apply_migrations(db)
    assert v1 == v2 == CURRENT_VERSION

    async with db.execute("SELECT COUNT(*) FROM schema_version") as cursor:
        row = await cursor.fetchone()
    # Should not insert duplicate version rows
    assert row[0] == 1


async def test_get_current_version_after_apply(db):
    await apply_migrations(db)
    version = await get_current_version(db)
    assert version == CURRENT_VERSION
