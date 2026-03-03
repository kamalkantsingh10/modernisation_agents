from pathlib import Path

from delta_macros_mcp.result import make_error, make_result, make_warning


def _parse_macro_file(path: Path) -> dict | None:
    """Parse a macro .md file into a structured dict. Returns None on error."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None

    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    def _section(key: str) -> str:
        return "\n".join(sections.get(key, [])).strip()

    # Parse parameter table from ## Parameters section
    parameters: list[dict] = []
    param_lines = sections.get("Parameters", [])
    table_rows = [l for l in param_lines if l.strip().startswith("|")]
    # row 0 = header, row 1 = separator, row 2+ = data
    for row in table_rows[2:]:
        cols = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cols) >= 3:
            parameters.append(
                {"name": cols[0], "type": cols[1], "description": cols[2]}
            )

    # Derive name from filename stem
    name = path.stem

    return {
        "name": name,
        "purpose": _section("Purpose"),
        "parameters": parameters,
        "returns": _section("Returns"),
        "category": _section("Category"),
        "example_usage": _section("Example Usage"),
        "notes": _section("Notes"),
    }


def _find_macro_file(name: str, library_path: Path) -> Path | None:
    """Look for <library_path>/<name>.md then <library_path>/<name.upper()>.md."""
    exact = library_path / f"{name}.md"
    if exact.exists():
        return exact
    upper = library_path / f"{name.upper()}.md"
    if upper.exists():
        return upper
    return None


def get_macro(name: str, library_path: Path) -> dict:
    """Return the structured macro definition for *name*, or a warning if not found."""
    path = _find_macro_file(name, library_path)
    if path is None:
        return make_warning(
            data=None,
            message="Macro not found",
            flags=[
                {
                    "code": "UNKNOWN_MACRO",
                    "message": f"No macro definition found for '{name}'",
                    "location": name,
                }
            ],
        )
    parsed = _parse_macro_file(path)
    if parsed is None:
        return make_warning(
            data=None,
            message="Macro file could not be parsed",
            flags=[
                {
                    "code": "UNKNOWN_MACRO",
                    "message": f"Could not parse macro file for '{name}'",
                    "location": name,
                }
            ],
        )
    return make_result(data=parsed)


def search_macros(keyword: str, library_path: Path) -> dict:
    """Return lightweight summaries of macros whose name or purpose matches *keyword*."""
    keyword_lower = keyword.lower()
    matches = []
    for md_file in sorted(library_path.glob("*.md")):
        parsed = _parse_macro_file(md_file)
        if parsed is None:
            continue
        if keyword_lower in parsed["name"].lower() or keyword_lower in parsed["purpose"].lower():
            matches.append(
                {
                    "name": parsed["name"],
                    "purpose": parsed["purpose"],
                    "category": parsed["category"],
                }
            )
    return make_result(data=matches)


def list_categories(library_path: Path) -> dict:
    """Return a sorted, deduplicated list of all category values in the library."""
    categories: set[str] = set()
    for md_file in library_path.glob("*.md"):
        parsed = _parse_macro_file(md_file)
        if parsed is None:
            continue
        cat = parsed.get("category", "")
        if cat:
            categories.add(cat)
    return make_result(data=sorted(categories))


# ── Story 2.2 additions ────────────────────────────────────────────────────────

import re  # noqa: E402


def _validate_macro_name(name: str) -> str | None:
    """Return None if valid, or an error message string if invalid."""
    if not name or not name.strip():
        return "Macro name must not be empty or whitespace"
    if not re.fullmatch(r"[A-Z0-9\-]+", name.strip().upper()):
        return (
            "Macro name may only contain uppercase letters, digits, and hyphens"
        )
    return None


def _render_macro_file(
    name: str,
    purpose: str,
    parameters: list[dict],
    returns: str,
    category: str,
) -> str:
    """Render the full markdown content for a macro file."""
    lines = [
        f"## Name",
        f"",
        f"`{name}`",
        f"",
        f"## Purpose",
        f"",
        purpose,
        f"",
        f"## Parameters",
        f"",
        "| Parameter | Type | Description |",
        "|-----------|------|-------------|",
    ]
    for param in parameters:
        lines.append(
            f"| {param.get('name', '')} | {param.get('type', '')} | {param.get('description', '')} |"
        )
    lines += [
        f"",
        f"## Returns",
        f"",
        returns,
        f"",
        f"## Category",
        f"",
        category if category else "(none)",
        f"",
        f"## Example Usage",
        f"",
        f"```cobol",
        f"CALL '{name}' USING WS-PARAM.",
        f"```",
        f"",
        f"## Notes",
        f"",
        f"",
    ]
    return "\n".join(lines)


def add_macro(
    name: str,
    purpose: str,
    parameters: list[dict],
    returns: str,
    category: str,
    library_path: Path,
) -> dict:
    """Write (create or overwrite) a macro markdown file in *library_path*."""
    error_msg = _validate_macro_name(name)
    if error_msg:
        return make_error(f"Invalid macro name: {error_msg}")

    normalised_name = name.strip().upper()
    target_path = library_path / f"{normalised_name}.md"

    content = _render_macro_file(normalised_name, purpose, parameters, returns, category)
    try:
        target_path.write_text(content, encoding="utf-8")
    except OSError as e:
        return make_error(f"Failed to write macro file: {e}")

    return make_result(
        data={"file": str(target_path)},
        message=f"Macro {normalised_name} written to {target_path}",
    )
