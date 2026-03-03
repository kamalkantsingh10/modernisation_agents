import logging
from pathlib import Path

from fastmcp import FastMCP

from cobol_parser_mcp import (
    antipattern_detector,
    call_graph,
    cluster_builder,
    cobol_parser,
    complexity_scorer,
)

_log_dir = Path("logs")
_log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(_log_dir / "cobol-parser-mcp.log"),
    ],
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP("cobol-parser-mcp", version="0.1.0")


@mcp.tool()
def parse_module(program_name: str, source_path: str) -> dict:
    """Parse a COBOL source file and return structural metadata: paragraphs with line
    numbers, COPY references, CALL targets, EXEC SQL/CICS block locations, and Delta
    macro invocations.  Stores the result in the session cache keyed by PROGRAM-ID."""
    return cobol_parser.parse_module(program_name, source_path)


@mcp.tool()
def extract_call_graph(program_name: str) -> dict:
    """Extract the directed PERFORM call graph for a previously parsed COBOL module.
    Returns nodes (paragraph names) and edges (PERFORM relationships), with THRU
    ranges fully expanded. Requires parse_module to have been called first."""
    return call_graph.build_call_graph(program_name)


@mcp.tool()
def score_complexity(program_name: str) -> dict:
    """Return a complexity rating (Low / Medium / High) and contributing factors for a
    previously parsed COBOL module: paragraph count, maximum PERFORM nesting depth,
    REDEFINES count, and GO TO count. Requires parse_module to have been called first."""
    return complexity_scorer.score_complexity(program_name)


@mcp.tool()
def detect_antipatterns(program_name: str) -> dict:
    """Detect structural anti-patterns in a previously parsed COBOL module: GOTO, ALTER,
    NESTED_PERFORM_THRU, REDEFINES_NON_FILLER, and FALLTHROUGH_PARAGRAPH. EXEC CICS and
    EXEC SQL constructs are reported in the flags array. Requires parse_module first."""
    return antipattern_detector.detect_antipatterns(program_name)


@mcp.tool()
def build_cluster_context(program_name: str) -> dict:
    """Assemble a privacy-safe context object (paragraph names, PERFORM edges, DATA
    DIVISION field names — NO raw source) for the Viper agent to use when performing
    LLM-based semantic paragraph clustering. Requires parse_module first."""
    return cluster_builder.build_cluster_context(program_name)


@mcp.tool()
def validate_cluster_output(program_name: str, clusters: list) -> dict:
    """Validate cluster groupings produced by the Viper agent: checks non-empty names,
    and that all referenced paragraphs exist in the parsed module. Stores valid clusters
    in session cache for the Viper workflow to write to the spec layer."""
    return cluster_builder.validate_cluster_output(program_name, clusters)


if __name__ == "__main__":
    mcp.run()
