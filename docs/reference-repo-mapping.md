# Reference Repo — Design Mapping

When designing a component, consult the files listed below from the reference repository.

**Repo:** [Azure-Samples/Legacy-Modernization-Agents](https://github.com/Azure-Samples/Legacy-Modernization-Agents)
**Base raw URL:** `https://raw.githubusercontent.com/Azure-Samples/Legacy-Modernization-Agents/main/`

---

## Viper — COBOL Structural Analyst

| File | What to look for |
|---|---|
| `Agents/CobolAnalyzerAgent.cs` | How the agent is structured, API call pattern, fallback handling, parallelisation |
| `Agents/Prompts/CobolAnalyzer.md` | The actual system + user prompt — what the AI is asked to extract |
| `Models/CobolAnalysis.cs` | Output data model — fields returned from analysis |
| `Models/CobolFile.cs` | Input model — how a COBOL file is represented |
| `Chunking/Core/SemanticUnitChunker.cs` | Their chunking algorithm (structural boundaries) — we improve on this with semantic clustering |
| `Chunking/Adapters/CobolAdapter.cs` | How COBOL-specific chunking boundaries are detected |
| `Chunking/Context/ChunkContextManager.cs` | How context (e.g. DATA DIVISION) is preserved across chunks |
| `Chunking/ChunkingOrchestrator.cs` | How chunking and conversion are orchestrated together |
| `Agents/Infrastructure/AgentBase.cs` | Base agent pattern — API selection, prompt loading, error handling |
| `Agents/Infrastructure/ChatClientFactory.cs` | How AI clients are configured and selected |

---

## Crane — Dependency Mapper

| File | What to look for |
|---|---|
| `Agents/DependencyMapperAgent.cs` | Regex patterns for COPY/CALL/SQL/CICS extraction, deduplication logic |
| `Agents/Prompts/DependencyMapper.md` | What the AI analyses on top of the extracted graph |
| `Models/DependencyMap.cs` | Output model — what a dependency map contains |
| `Persistence/SqliteMigrationRepository.cs` | `dependencies` and `metrics` table schema and insert logic |

---

## Shifu — Business Logic Extractor

| File | What to look for |
|---|---|
| `Agents/BusinessLogicExtractorAgent.cs` | How business logic is extracted, chunking for large files, merge strategy |
| `Agents/Prompts/BusinessLogicExtractor.md` | The prompt — "WHAT not HOW", use case format, glossary injection pattern |
| `Models/BusinessLogic.cs` | Output model — BusinessPurpose, UserStories, Features, BusinessRules structure |
| `Data/glossary.json` | Format of the glossary — how it is structured for prompt injection |
| `Persistence/SqliteMigrationRepository.cs` | All `spec_*` table schemas — this is the spec layer we populate |

---

## Spec Layer (Intermediate Representation)

| File | What to look for |
|---|---|
| `Persistence/SqliteMigrationRepository.cs` | Full spec layer table definitions: `spec_rosetta_dictionary`, `spec_data_entities`, `spec_data_fields`, `spec_business_rules`, `spec_service_definitions`, `spec_service_operations`, `spec_operation_inputs`, `spec_operation_rules` |
| `docs/spec-approach-concept.md` | Conceptual explanation of the spec layer and why it exists |
| `Persistence/IMigrationRepository.cs` | Repository interface — all read/write operations available |

---

## Storage / Database

| File | What to look for |
|---|---|
| `Persistence/SqliteMigrationRepository.cs` | Full SQLite schema (17 tables), all CREATE TABLE statements, insert and query patterns |
| `Persistence/IMigrationRepository.cs` | Interface — what operations the storage layer must support |
| `Persistence/HybridMigrationRepository.cs` | How they tried to support both SQLite and Neo4j (useful to understand why we skip Neo4j) |
| `Persistence/Neo4jMigrationRepository.cs` | The Neo4j attempt — confirms it was never fully implemented |

---

## Chunking Strategy

| File | What to look for |
|---|---|
| `Chunking/Core/SemanticUnitChunker.cs` | Their structural boundary approach — division → section → paragraph priority ordering |
| `Chunking/Context/ChunkContextManager.cs` | How shared context (data definitions) is injected into each chunk |
| `Chunking/Core/SignatureRegistry.cs` | Tracking COBOL paragraphs → target method signatures across chunks |
| `Chunking/Core/TypeMappingTable.cs` | COBOL type → target language type mappings |
| `Chunking/Models/UnifiedIR.cs` | Intermediate representation used between chunks |
| `Chunking/Validation/ConversionValidator.cs` | How chunk output is validated before merging |
| `docs/Smart-chuncking-how it-works.md` | Plain English explanation of their chunking approach |
| `docs/smart-chunking-architecture.md` | Architecture diagram of the chunking system |
| `CobolToQuarkusMigration.Tests/Chunking/` | Tests — good for understanding expected behaviour of each chunking component |

---

## Pipeline / Orchestration

| File | What to look for |
|---|---|
| `Processes/SmartMigrationOrchestrator.cs` | Top-level pipeline — how agents are sequenced and parallelised |
| `Processes/MigrationProcess.cs` | Full migration run (analysis + conversion) |
| `Processes/ReverseEngineeringProcess.cs` | Analysis-only mode (no conversion) — closest to what our analysis agents do |
| `Processes/ChunkedMigrationProcess.cs` | How chunked processing is orchestrated end-to-end |
| `Processes/ChunkedReverseEngineeringProcess.cs` | Chunked analysis-only mode |
| `docs/legacy-modernization-flow.md` | End-to-end flow diagram |
| `docs/REVERSE_ENGINEERING_ARCHITECTURE.md` | Architecture of the analysis-only path |
| `Program.cs` | Entry point — how modes (migrate / reverse-engineer / mcp-server) are selected |

---

## delta-macros-mcp (Middleware Knowledge Server)

| File | What to look for |
|---|---|
| `Mcp/` folder | Their MCP server implementation — tools exposed, how it connects to the agent pipeline |
| `.vscode/mcp.json` | MCP server configuration — how it is registered and started |
| `Processes/RunMcpServerProcess.cs` | How the MCP server process is launched and managed |
| `McpChatWeb/` | Their web chat portal that uses MCP — useful for understanding MCP tool calling patterns |

---

## Po — Dev Agent (Target Code Generation reference)

| File | What to look for |
|---|---|
| `Agents/JavaConverterAgent.cs` | How Java conversion is prompted, how it consumes analysis output |
| `Agents/Prompts/JavaConverter.md` | Java conversion prompt — structure of generated code, framework choices |
| `Agents/ChunkAwareJavaConverter.cs` | How chunk-aware conversion maintains context across large programs |
| `Agents/Prompts/ChunkAwareJavaConverter.md` | Prompt for chunk-aware conversion — forward reference handling |
| `Chunking/Core/SignatureRegistry.cs` | How method signatures are tracked so chunks can call each other |
| `Chunking/Core/TypeMappingTable.cs` | COBOL → Java type mappings |

---

## Reference COBOL Sample Files

| File | What to look for |
|---|---|
| `source/CUSTOMER-INQUIRY.cbl` | Sample COBOL program — useful for testing Agent 1 prompts |
| `source/CUSTOMER-DISPLAY.cbl` | Second sample program — tests multi-program dependency mapping |
| `source/CUSTOMER-DATA.cpy` | Sample copybook — tests COPY statement handling |

---

## Key Docs to Read First

Before designing any component, read these in order:

1. `README.md` — overall system overview and quick start
2. `docs/legacy-modernization-flow.md` — the full pipeline diagram
3. `docs/REVERSE_ENGINEERING_ARCHITECTURE.md` — analysis-only mode architecture
4. `docs/spec-approach-concept.md` — why the spec layer exists
5. `docs/Smart-chuncking-how it-works.md` — plain English chunking explanation
