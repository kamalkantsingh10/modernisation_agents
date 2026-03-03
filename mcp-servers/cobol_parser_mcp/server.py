import logging
from pathlib import Path
from fastmcp import FastMCP

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

if __name__ == "__main__":
    mcp.run()
