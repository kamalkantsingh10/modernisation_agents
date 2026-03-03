import pytest
import aiosqlite
from specdb_mcp.schema import ALL_CREATE_STATEMENTS
from specdb_mcp import spec_db


@pytest.fixture
async def db():
    """In-memory SQLite database with schema applied."""
    async with aiosqlite.connect(":memory:") as database:
        for sql in ALL_CREATE_STATEMENTS:
            await database.execute(sql)
        await database.commit()
        yield database


# ── write_spec / read_spec ────────────────────────────────────────────────────

async def test_write_and_read_spec(db):
    await spec_db.write_spec(db, "cobol_files", "BJ-MAIN", {
        "source_path": "/src/BJ-MAIN.cbl",
        "line_count": 200,
    })
    rows = await spec_db.read_spec(db, "cobol_files", "BJ-MAIN")
    assert len(rows) == 1
    assert rows[0]["program_name"] == "BJ-MAIN"
    assert rows[0]["source_path"] == "/src/BJ-MAIN.cbl"
    assert rows[0]["line_count"] == 200


async def test_write_spec_idempotent(db):
    await spec_db.write_spec(db, "cobol_files", "BJ-MAIN", {
        "source_path": "/src/BJ-MAIN.cbl",
        "line_count": 200,
    })
    await spec_db.write_spec(db, "cobol_files", "BJ-MAIN", {
        "source_path": "/src/BJ-MAIN.cbl",
        "line_count": 250,  # updated
    })
    rows = await spec_db.read_spec(db, "cobol_files", "BJ-MAIN")
    assert len(rows) == 1
    assert rows[0]["line_count"] == 250


async def test_read_spec_empty_for_missing_program(db):
    rows = await spec_db.read_spec(db, "cobol_files", "NONEXISTENT")
    assert rows == []


async def test_write_spec_with_compound_identity(db):
    """spec_entities uses (program_name, entity_id) as identity key."""
    await spec_db.write_spec(db, "spec_entities", "BJ-MAIN", {
        "entity_id": "ENTITY-001",
        "entity_type": "Account",
        "description": "Player account",
    })
    await spec_db.write_spec(db, "spec_entities", "BJ-MAIN", {
        "entity_id": "ENTITY-001",
        "entity_type": "Account",
        "description": "Updated description",
    })
    rows = await spec_db.read_spec(db, "spec_entities", "BJ-MAIN")
    assert len(rows) == 1
    assert rows[0]["description"] == "Updated description"


# ── query_spec ────────────────────────────────────────────────────────────────

async def test_query_spec_returns_rows(db):
    await spec_db.write_spec(db, "cobol_files", "BJ-MAIN", {
        "source_path": "/src/BJ-MAIN.cbl",
    })
    rows = await spec_db.query_spec(
        db, "SELECT * FROM cobol_files WHERE program_name = ?", ["BJ-MAIN"]
    )
    assert len(rows) == 1
    assert rows[0]["program_name"] == "BJ-MAIN"


async def test_query_spec_empty_result(db):
    rows = await spec_db.query_spec(
        db, "SELECT * FROM cobol_files WHERE program_name = ?", ["NOBODY"]
    )
    assert rows == []


# ── validation ────────────────────────────────────────────────────────────────

async def test_invalid_table_raises_value_error_on_write(db):
    with pytest.raises(ValueError, match="Unknown table"):
        await spec_db.write_spec(db, "evil_table; DROP TABLE cobol_files", "X", {})


async def test_invalid_table_raises_value_error_on_read(db):
    with pytest.raises(ValueError, match="Unknown table"):
        await spec_db.read_spec(db, "not_a_real_table", "BJ-MAIN")


async def test_read_spec_raises_for_dependencies_table(db):
    """dependencies has no program_name column — read_spec must reject it."""
    with pytest.raises(ValueError, match="read_spec does not support 'dependencies'"):
        await spec_db.read_spec(db, "dependencies", "BJ-MAIN")


async def test_transaction_rollback_leaves_no_data(db):
    """A failed write must not leave partial data in the DB."""
    # Cause a failure mid-transaction by passing a non-existent column
    try:
        await spec_db.write_spec(db, "cobol_files", "BJ-FAIL", {
            "nonexistent_column": "bad"
        })
    except Exception:
        pass

    rows = await spec_db.read_spec(db, "cobol_files", "BJ-FAIL")
    assert rows == [], "Rolled-back transaction must not persist any data"


async def test_all_allowed_tables_are_writable(db):
    """Smoke-test: each allowed table accepts a write without crashing."""
    writes = [
        ("cobol_files", "PROG-A", {"source_path": "/a.cbl"}),
        ("analyses", "PROG-A", {"division_structure": "{}"}),
        ("metrics", "PROG-A", {"complexity_score": "Low"}),
        ("dependencies", "PROG-A", {
            "source_program": "PROG-A",
            "target_program": "PROG-B",
            "dependency_type": "CALL",
        }),
        ("spec_entities", "PROG-A", {"entity_id": "E-001", "entity_type": "Account"}),
        ("spec_operations", "PROG-A", {"operation_id": "OP-001", "operation_name": "Init"}),
        ("spec_rules", "PROG-A", {"rule_id": "RULE-001", "rule_type": "Validation"}),
        ("spec_data_flows", "PROG-A", {"flow_id": "FLOW-001"}),
    ]
    for table, program_name, fields in writes:
        await spec_db.write_spec(db, table, program_name, fields)
