# server.py
import os
from pathlib import Path
import sys

# Ensure project root is in python path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

# Compatible with both mcp 2.x (MCPServer) and mcp 1.x (FastMCP)
try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

from main import generate_cv

mcp = FastMCP("Overleaf CV Compiler")


@mcp.tool()
def compile_cv(
    role: str,
    latex_content: str,
    project_id: str = None,
    candidate_name: str = None,
) -> str:
    """Compile a tailored LaTeX resume into a PDF via Overleaf and save it locally.

    Args:
        role: Target role slug (e.g. 'Agent_Dev', 'AI_Engineer', 'Fullstack').
        latex_content: The full, tailored LaTeX source code of the resume.
        project_id: Optional Overleaf project ID override if different from .env.
        candidate_name: Optional candidate name override if different from .env.

    Returns:
        The local file path where the compiled PDF is saved.
    """
    try:
        pdf_path = generate_cv(
            role=role,
            latex_source=latex_content,
            project_id=project_id,
            candidate_name=candidate_name,
            out_dir=str(PROJECT_ROOT / "out"),
        )
        abs_path = os.path.abspath(pdf_path)
        return f"SUCCESS: PDF compiled and saved to: {abs_path}"
    except Exception as e:
        return f"ERROR compiling CV on Overleaf: {str(e)}"


if __name__ == "__main__":
    mcp.run()
