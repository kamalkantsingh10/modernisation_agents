import logging
import re
from contextlib import asynccontextmanager
from pathlib import Path
from sqlite3 import OperationalError

import aiosqlite
from fastmcp import FastMCP

from .config import load_config
from .result import make_result, make_error
from .schema import ALL_CREATE_STATEMENTS
from .migrations import apply_migrations
from . import spec_db as _spec_db

_log_dir = Path("logs")
_log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(_log_dir / "specdb-mcp.log"),
    ],
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(server):
    try:
        config = load_config()
        db_path = config["db_path"]
        async with aiosqlite.connect(db_path) as db:
            await apply_migrations(db)
    except Exception as e:
        logger.warning("Startup migration check failed (DB may not exist yet): %s", e)
    yield


mcp = FastMCP("specdb-mcp", version="0.1.0", lifespan=lifespan)


@mcp.tool()
async def init_schema() -> dict:
    """Initialise the SQLite spec layer schema. Safe to call multiple times (idempotent)."""
    try:
        config = load_config()
        db_path = config["db_path"]
        async with aiosqlite.connect(db_path) as db:
            tables_created = []
            for sql in ALL_CREATE_STATEMENTS:
                await db.execute(sql)
                match = re.search(
                    r"CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+(\w+)", sql, re.IGNORECASE
                )
                tables_created.append(match.group(1) if match else "unknown")
            await db.commit()
            version = await apply_migrations(db)
        return make_result(
            data={"tables_created": tables_created, "schema_version": version},
            message=f"Schema initialised at version {version}",
        )
    except OperationalError as e:
        return make_error(f"Database error (check db_path is writable): {e}")
    except Exception as e:
        return make_error(f"Schema initialisation failed: {e}")


@mcp.tool()
async def write_spec(table: str, program_name: str, fields: dict) -> dict:
    """Write or update a record in the spec layer using idempotent upsert."""
    try:
        config = load_config()
        async with aiosqlite.connect(config["db_path"]) as db:
            await _spec_db.write_spec(db, table, program_name, fields)
        return make_result(
            data={"table": table, "program_name": program_name},
            message=f"Spec written to {table} for {program_name}",
        )
    except ValueError as e:
        return make_error(str(e))
    except Exception as e:
        return make_error(f"write_spec failed: {e}")


@mcp.tool()
async def read_spec(table: str, program_name: str) -> dict:
    """Read all spec records for a program from a given table."""
    try:
        config = load_config()
        async with aiosqlite.connect(config["db_path"]) as db:
            rows = await _spec_db.read_spec(db, table, program_name)
        return make_result(data=rows, message=f"Found {len(rows)} record(s)")
    except ValueError as e:
        return make_error(str(e))
    except Exception as e:
        return make_error(f"read_spec failed: {e}")


@mcp.tool()
async def query_spec(sql_fragment: str, params: list | None = None) -> dict:
    """Execute a parameterised SELECT query against the spec layer.

    sql_fragment must be a full SELECT statement. params is a list of bind values.
    WARNING: sql_fragment is passed directly to SQLite — always use parameterised
    queries with the params list; never interpolate user values into sql_fragment.
    """
    if not sql_fragment.strip().upper().startswith("SELECT"):
        return make_error("query_spec only supports SELECT statements")
    try:
        config = load_config()
        async with aiosqlite.connect(config["db_path"]) as db:
            rows = await _spec_db.query_spec(db, sql_fragment, params)
        return make_result(data=rows, message=f"Query returned {len(rows)} row(s)")
    except Exception as e:
        return make_error(f"query_spec failed: {e}")


if __name__ == "__main__":
    mcp.run()
