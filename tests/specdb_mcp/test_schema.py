import asyncio
import pytest
import aiosqlite
from specdb_mcp.schema import ALL_CREATE_STATEMENTS

EXPECTED_TABLES = {
    "schema_version",
    "cobol_files",
    "analyses",
    "metrics",
    "dependencies",
    "spec_entities",
    "spec_operations",
    "spec_rules",
    "spec_data_flows",
}


@pytest.fixture
async def db():
    async with aiosqlite.connect(":memory:") as database:
        yield database


async def test_all_nine_tables_created(db):
    for sql in ALL_CREATE_STATEMENTS:
        await db.execute(sql)
    await db.commit()

    async with db.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ) as cursor:
        rows = await cursor.fetchall()
    created = {row[0] for row in rows if not row[0].startswith("sqlite_")}
    assert EXPECTED_TABLES == created


async def test_idempotent_double_creation(db):
    for sql in ALL_CREATE_STATEMENTS:
        await db.execute(sql)
    await db.commit()
    # Second call must not raise
    for sql in ALL_CREATE_STATEMENTS:
        await db.execute(sql)
    await db.commit()


async def test_all_statements_use_if_not_exists():
    for sql in ALL_CREATE_STATEMENTS:
        normalised = " ".join(sql.upper().split())
        assert "CREATE TABLE IF NOT EXISTS" in normalised, (
            f"Missing IF NOT EXISTS in: {sql[:80]}"
        )


async def test_nine_statements_present():
    assert len(ALL_CREATE_STATEMENTS) == 9
