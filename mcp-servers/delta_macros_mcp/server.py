import logging
from pathlib import Path
from fastmcp import FastMCP

from delta_macros_mcp import macro_library
from delta_macros_mcp.config import _find_project_root, load_config
from delta_macros_mcp.result import make_error

_log_dir = Path("logs")
_log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(_log_dir / "delta-macros-mcp.log"),
    ],
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP("delta-macros-mcp", version="0.1.0")


def _resolve_library_path() -> Path | None:
    """Resolve macro_library_path from config, returning None if not found."""
    config = load_config()
    return _find_project_root() / config["macro_library_path"]


@mcp.tool()
def get_macro(macro_name: str) -> dict:
    """Look up a macro definition by name."""
    logger.info("get_macro called: macro_name=%s", macro_name)
    try:
        library_path = _resolve_library_path()
        if not library_path.exists():
            return make_error(f"Macro library not found: {library_path}")
        return macro_library.get_macro(macro_name, library_path)
    except Exception as e:
        return make_error(f"Unexpected error in get_macro: {e}")


@mcp.tool()
def search_macros(keyword: str) -> dict:
    """Search macro definitions by keyword (matches name and purpose)."""
    logger.info("search_macros called: keyword=%s", keyword)
    try:
        library_path = _resolve_library_path()
        if not library_path.exists():
            return make_error(f"Macro library not found: {library_path}")
        return macro_library.search_macros(keyword, library_path)
    except Exception as e:
        return make_error(f"Unexpected error in search_macros: {e}")


@mcp.tool()
def list_categories() -> dict:
    """List all macro category groupings present in the library."""
    logger.info("list_categories called")
    try:
        library_path = _resolve_library_path()
        if not library_path.exists():
            return make_error(f"Macro library not found: {library_path}")
        return macro_library.list_categories(library_path)
    except Exception as e:
        return make_error(f"Unexpected error in list_categories: {e}")


@mcp.tool()
def add_macro(
    macro_name: str,
    purpose: str,
    parameters: list,
    returns: str,
    category: str = "",
) -> dict:
    """Add or update a macro definition in the library."""
    logger.info("add_macro called: macro_name=%s", macro_name)
    try:
        library_path = _resolve_library_path()
        if not library_path.exists():
            return make_error(f"Macro library directory not found: {library_path}")
        return macro_library.add_macro(macro_name, purpose, parameters, returns, category, library_path)
    except Exception as e:
        return make_error(f"Unexpected error in add_macro: {e}")


if __name__ == "__main__":
    mcp.run()
