import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

CURRENT_VERSION = 1

MIGRATIONS: dict[int, list[str]] = {
    1: [
        # Initial schema — tables are created in schema.py.
        # This migration just records version 1 as applied.
    ],
    # Future migrations go here:
    # 2: ["ALTER TABLE cobol_files ADD COLUMN ..."],
}


async def get_current_version(db) -> int:
    """Returns 0 if schema_version table is empty or missing."""
    try:
        async with db.execute("SELECT MAX(version) FROM schema_version") as cursor:
            row = await cursor.fetchone()
            return row[0] if row and row[0] is not None else 0
    except Exception:
        return 0


async def apply_migrations(db) -> int:
    """Applies all pending migrations in order. Returns current version."""
    current = await get_current_version(db)
    for version, statements in sorted(MIGRATIONS.items()):
        if version > current:
            logger.info("Applying migration to version %d", version)
            for sql in statements:
                await db.execute(sql)
            now = datetime.now(timezone.utc).isoformat()
            await db.execute(
                "INSERT INTO schema_version (version, applied_at) VALUES (?, ?)",
                (version, now),
            )
            await db.commit()
            logger.info("Migration to version %d applied", version)
    return CURRENT_VERSION
