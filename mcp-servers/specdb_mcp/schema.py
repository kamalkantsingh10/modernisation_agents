ALL_CREATE_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS schema_version (
        id INTEGER PRIMARY KEY,
        version INTEGER NOT NULL,
        applied_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS cobol_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_name TEXT NOT NULL UNIQUE,
        source_path TEXT NOT NULL,
        file_size_bytes INTEGER,
        line_count INTEGER,
        created_at TEXT NOT NULL DEFAULT '',
        updated_at TEXT NOT NULL DEFAULT ''
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_name TEXT NOT NULL,
        division_structure TEXT,
        paragraph_list TEXT,
        call_graph TEXT,
        external_refs TEXT,
        created_at TEXT NOT NULL DEFAULT '',
        updated_at TEXT NOT NULL DEFAULT '',
        FOREIGN KEY (program_name) REFERENCES cobol_files(program_name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_name TEXT NOT NULL,
        complexity_score TEXT NOT NULL,
        paragraph_count INTEGER,
        goto_count INTEGER,
        nested_perform_depth INTEGER,
        antipatterns TEXT,
        created_at TEXT NOT NULL DEFAULT '',
        updated_at TEXT NOT NULL DEFAULT '',
        FOREIGN KEY (program_name) REFERENCES cobol_files(program_name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS dependencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_program TEXT NOT NULL,
        target_program TEXT NOT NULL,
        dependency_type TEXT NOT NULL,
        location TEXT,
        created_at TEXT NOT NULL DEFAULT '',
        FOREIGN KEY (source_program) REFERENCES cobol_files(program_name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS spec_entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_name TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        description TEXT,
        source_paragraph TEXT,
        created_at TEXT NOT NULL DEFAULT '',
        updated_at TEXT NOT NULL DEFAULT '',
        UNIQUE(program_name, entity_id),
        FOREIGN KEY (program_name) REFERENCES cobol_files(program_name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS spec_operations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_name TEXT NOT NULL,
        operation_id TEXT NOT NULL,
        operation_name TEXT NOT NULL,
        description TEXT,
        source_paragraph TEXT,
        created_at TEXT NOT NULL DEFAULT '',
        updated_at TEXT NOT NULL DEFAULT '',
        UNIQUE(program_name, operation_id),
        FOREIGN KEY (program_name) REFERENCES cobol_files(program_name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS spec_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_name TEXT NOT NULL,
        rule_id TEXT NOT NULL,
        rule_type TEXT NOT NULL,
        description TEXT,
        source_paragraph TEXT,
        created_at TEXT NOT NULL DEFAULT '',
        updated_at TEXT NOT NULL DEFAULT '',
        UNIQUE(program_name, rule_id),
        FOREIGN KEY (program_name) REFERENCES cobol_files(program_name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS spec_data_flows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_name TEXT NOT NULL,
        flow_id TEXT NOT NULL,
        from_entity TEXT,
        to_entity TEXT,
        transformation TEXT,
        source_paragraph TEXT,
        created_at TEXT NOT NULL DEFAULT '',
        updated_at TEXT NOT NULL DEFAULT '',
        UNIQUE(program_name, flow_id),
        FOREIGN KEY (program_name) REFERENCES cobol_files(program_name)
    )
    """,
]
