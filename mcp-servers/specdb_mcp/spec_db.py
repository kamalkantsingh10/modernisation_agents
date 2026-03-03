from datetime import datetime, timezone

ALLOWED_TABLES = {
    "cobol_files",
    "analyses",
    "metrics",
    "dependencies",
    "spec_entities",
    "spec_operations",
    "spec_rules",
    "spec_data_flows",
}

# dependencies uses source_program/target_program instead of program_name,
# and has no updated_at column.
TABLES_WITH_PROGRAM_NAME = ALLOWED_TABLES - {"dependencies"}
TABLES_WITH_UPDATED_AT = ALLOWED_TABLES - {"dependencies"}

# Identity columns per table — used to determine the unique key for upsert.
IDENTITY_COLUMNS: dict[str, tuple[str, ...]] = {
    "cobol_files":     ("program_name",),
    "analyses":        ("program_name",),
    "metrics":         ("program_name",),
    "dependencies":    ("source_program", "target_program", "dependency_type"),
    "spec_entities":   ("program_name", "entity_id"),
    "spec_operations": ("program_name", "operation_id"),
    "spec_rules":      ("program_name", "rule_id"),
    "spec_data_flows": ("program_name", "flow_id"),
}


async def write_spec(db, table: str, program_name: str, fields: dict) -> None:
    """Idempotent upsert: INSERT OR IGNORE creates the row; UPDATE refreshes fields."""
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Unknown table: {table!r}")

    now = datetime.now(timezone.utc).isoformat()
    all_fields = dict(fields)
    if table in TABLES_WITH_PROGRAM_NAME:
        all_fields = {"program_name": program_name, **all_fields}
    if table in TABLES_WITH_UPDATED_AT:
        all_fields["updated_at"] = now

    columns = list(all_fields.keys())
    placeholders = ", ".join("?" for _ in columns)
    insert_sql = (
        f"INSERT OR IGNORE INTO {table} ({', '.join(columns)}, created_at) "
        f"VALUES ({placeholders}, ?)"
    )
    insert_values = list(all_fields.values()) + [now]

    identity_cols = IDENTITY_COLUMNS.get(table, ("program_name",))
    update_pairs = [
        (col, val)
        for col, val in all_fields.items()
        if col not in identity_cols and col != "created_at"
    ]
    set_clause = ", ".join(f"{col} = ?" for col, _ in update_pairs)
    where_clause = " AND ".join(f"{col} = ?" for col in identity_cols)
    update_sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    update_values = [val for _, val in update_pairs] + [
        all_fields[col] for col in identity_cols
    ]

    try:
        await db.execute("BEGIN")
        await db.execute(insert_sql, insert_values)
        if update_pairs:
            await db.execute(update_sql, update_values)
        await db.execute("COMMIT")
    except Exception:
        await db.execute("ROLLBACK")
        raise


async def read_spec(db, table: str, program_name: str) -> list[dict]:
    """Returns all rows for program_name as list of dicts. Empty list if none found."""
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Unknown table: {table!r}")
    if table not in TABLES_WITH_PROGRAM_NAME:
        raise ValueError(
            f"read_spec does not support '{table}' — it has no program_name column. "
            "Use query_spec with an explicit WHERE clause instead."
        )
    async with db.execute(
        f"SELECT * FROM {table} WHERE program_name = ?", (program_name,)
    ) as cursor:
        rows = await cursor.fetchall()
        col_names = [d[0] for d in cursor.description] if cursor.description else []
        return [dict(zip(col_names, row)) for row in rows]


async def query_spec(db, sql_fragment: str, params: list | None = None) -> list[dict]:
    """Execute a parameterised SELECT. sql_fragment must be a full SELECT statement."""
    async with db.execute(sql_fragment, params or []) as cursor:
        rows = await cursor.fetchall()
        col_names = [d[0] for d in cursor.description] if cursor.description else []
        return [dict(zip(col_names, row)) for row in rows]
