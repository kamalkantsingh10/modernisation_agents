# Story 1.4: Engagement Configuration & Templates

Status: done

## Story

As an **operator**,
I want a glossary template, macro library template, and clear config schema,
So that I can configure any new client engagement in under an hour with no code changes.

## Acceptance Criteria

1. **Given** the project is scaffolded (Story 1.1) **When** an operator opens `config.yaml` **Then** all required fields are present and documented with inline comments and example values: `db_path`, `macro_library_path`, `gitlab_url`, `project_name`, `target_language`.
2. **When** an operator opens `templates/glossary-template.md` **Then** it contains a markdown table with header `| COBOL Name | Business Term |` and at least 2 example rows, with clear instructions for population (NFR20).
3. **When** an operator opens `templates/macro-template.md` **Then** it is a human-readable markdown template with sections for macro `Name`, `Purpose`, `Parameters`, `Returns`, and `Example Usage` — ready for an operator to populate (NFR20).
4. **When** an operator opens `blackjack/glossary.md` **Then** it contains populated BlackJack field-name-to-business-term mappings (at minimum 10 COBOL field names mapped to business terms) — a working example, not empty.
5. **Given** `blackjack/` directory **Then** it contains both `glossary.md` (AC4) and a `macros/` subdirectory (can be empty or contain sample macro docs).
6. **Given** `templates/` directory **Then** it contains `glossary-template.md` (AC2) and `macro-template.md` (AC3).
7. **Given** any operator who reads `config.yaml` **Then** the `target_language` field has a comment explaining it is TBD and will be set before the Oogway stage — it must NOT be hardcoded to a specific language.

## Tasks / Subtasks

- [x] Task 1: Finalise `config.yaml` with full schema and inline documentation (AC: 1, 7)
  - [x] All 5 required fields present with example values
  - [x] Each field has an inline YAML comment explaining purpose
  - [x] `target_language` commented as "# TBD — set to 'Java' or 'Python' before Oogway stage"
- [x] Task 2: Create `templates/glossary-template.md` (AC: 2)
  - [x] Markdown table with `| COBOL Name | Business Term |` header
  - [x] At least 2 example rows
  - [x] Instructions section explaining how to populate
- [x] Task 3: Create `templates/macro-template.md` (AC: 3)
  - [x] Sections: Name, Purpose, Parameters, Returns, Example Usage
  - [x] Brief explanation of Delta macro concept at top
- [x] Task 4: Create `blackjack/glossary.md` with populated mappings (AC: 4)
  - [x] 15 COBOL field name → business term entries (exceeds minimum 10)
  - [x] Drawn from BlackJack domain
- [x] Task 5: Create `blackjack/macros/` directory (AC: 5)
  - [x] `blackjack/macros/.gitkeep`
- [x] Task 6: Verify all directories exist with correct structure
  - [x] `templates/`
  - [x] `blackjack/`
  - [x] `blackjack/macros/`

## Dev Notes

### Architecture Guardrails

- This story is **file creation only** — no Python code changes.
- `target_language` remains blank/TBD.

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Completion Notes List

- `config.yaml` at project root with all 5 fields + inline comments
- `templates/glossary-template.md` with 4 example rows and instructions
- `templates/macro-template.md` with all required sections
- `blackjack/glossary.md` with 15 populated entries
- `blackjack/macros/.gitkeep`

### File List

- `config.yaml`
- `templates/glossary-template.md`
- `templates/macro-template.md`
- `blackjack/glossary.md`
- `blackjack/macros/.gitkeep`
