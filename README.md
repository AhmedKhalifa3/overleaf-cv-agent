# 🚀 Overleaf CV Agent

[![M8ven Score](https://m8ven.ai/badge/mcp/ahmedkhalifa3-overleaf-cv-agent-112ble?v=ebdbc289a289d8e6bd511d6c20e8ba5e)](https://m8ven.ai/mcp/ahmedkhalifa3-overleaf-cv-agent-112ble?s=readme)

> Turn Claude, Cursor, Windsurf, or any AI into an autonomous CV tailoring agent that tailors your LaTeX resume to any job description and compiles ready-to-send PDFs in seconds via Overleaf.

---

## 💡 How It Works

```
┌────────────────────────────────────────────────────────┐
│  AI Assistant (Claude Desktop / Cursor / Windsurf)     │
│  • Reads your base cv.tex from Project Knowledge       │
│  • Analyzes target Job Description                     │
│  • Rewrites & tailors LaTeX to match role requirements │
└───────────────────────────┬────────────────────────────┘
                            │ 1. Invokes tool: compile_cv(role, latex)
                            ▼
┌────────────────────────────────────────────────────────┐
│  Local FastMCP Server (server.py)                      │
│  • Receives tailored LaTeX from AI                     │
│  • Validates and cleans markdown artifacts             │
└───────────────────────────┬────────────────────────────┘
                            │ 2. Calls Overleaf API
                            ▼
┌────────────────────────────────────────────────────────┐
│  Overleaf Cloud Compiler (main.py)                     │
│  • Headless CLSI cloud compilation                     │
│  • Downloads resulting PDF & saves to out/             │
└───────────────────────────┬────────────────────────────┘
                            │ 3. Saved locally
                            ▼
┌────────────────────────────────────────────────────────┐
│  out/{Candidate}_Your_Next_{Role}.pdf                  │
└────────────────────────────────────────────────────────┘
```

---

## 📦 Quickstart Guide

### 1. Clone & Set Up Python Environment

```bash
git clone https://github.com/AhmedKhalifa3/overleaf-cv-agent.git
cd overleaf-cv-agent

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 2. Configure Credentials (`.env`)

Copy the example configuration:
```bash
cp .env.example .env
```

Edit `.env` with your values:
```env
OVERLEAF_SESSION='s%3A...'
OVERLEAF_PROJECT_ID='6abf1047f91f1b529a383659'
CANDIDATE_NAME='Your_Name'
CV_NAMING_TEMPLATE='{name}_Your_Next_{role}.pdf'
```

#### How to get your Overleaf credentials:
1. **`OVERLEAF_SESSION`**:
   - Log into [Overleaf](https://www.overleaf.com).
   - Press `F12` to open Developer Tools &rarr; **Application** tab (Chrome/Edge) or **Storage** tab (Firefox).
   - Expand **Cookies** &rarr; `https://www.overleaf.com`.
   - Copy the value of the **`overleaf_session2`** cookie.
   - **Why this is needed**: Overleaf does not provide public API keys for personal accounts. The `overleaf_session2` cookie acts as your authenticated session token, allowing the script to upload files, trigger compilation, and download PDFs headlessly in the background without needing a browser window.
   - **How to get it**:
     1. Log into [Overleaf](https://www.overleaf.com) in your browser.
     2. Press `F12` to open Developer Tools &rarr; select the **Application** tab (Chrome/Edge/Brave) or **Storage** tab (Firefox).
     3. In the left panel, expand **Cookies** &rarr; click `https://www.overleaf.com`.
     4. Find the cookie named **`overleaf_session2`** and copy its full value.
2. **`OVERLEAF_PROJECT_ID`**:
   - Open your Overleaf CV project.
   - Look at the browser URL: `https://www.overleaf.com/project/<PROJECT_ID>`.
   - Copy the 24-character ID.

---

### 3. Add Your Base Resume

Copy the provided sample template or place your own LaTeX resume as `cv.tex`:
```bash
cp cv.example.tex cv.tex
```
*(Note: `cv.tex` is included in `.gitignore` so your personal contact info will never be accidentally committed).*

---

## 🤖 Connecting Your AI Assistant

### Step A: Add Base CV & Instructions to Your AI's Context

Whether using **Claude Projects**, **Custom GPTs**, **Gemini Gems**, or **Cursor**:
1. **Upload your master resume** (`cv.tex`) to your AI's Project Knowledge / Files.
2. **Configure your AI Instructions / System Prompt**:
   - **Use your own instructions or ours**: You are completely free to write whatever custom prompts, tone, or tailoring guidelines you prefer.
   - **The only requirement**: You must explicitly instruct the AI to call the `compile_cv` tool once it finishes generating the LaTeX code. For example, add this line:
     > *"After tailoring the LaTeX code, call the `compile_cv` tool with the role slug and complete LaTeX code to compile and save the final PDF."*
   - Or, simply copy our ready-made, production-ready prompt from [`PROJECT_INSTRUCTIONS.md`](PROJECT_INSTRUCTIONS.md) which already includes strict 1-page budget rules and automatic compilation.

---

### Step B: Connect the Local MCP Server

#### Option 1: Claude Desktop

Edit your Claude Desktop configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the `cv-compiler` entry under `mcpServers`:

```json
{
  "mcpServers": {
    "cv-compiler": {
      "command": "/absolute/path/to/overleaf-cv-agent/.venv/bin/python",
      "args": ["/absolute/path/to/overleaf-cv-agent/server.py"]
    }
  }
}
```
*(On Windows, use python executable path like `"C:\\path\\to\\overleaf-cv-agent\\.venv\\Scripts\\python.exe"`)*

##### 🔄 Restarting Claude Desktop:
Claude Desktop only reads the configuration on a **full process launch**:
- **Linux**: Note that the binary name is `claude-desktop` (not `claude`). Fully restart with:
  ```bash
  pkill -f claude-desktop
  claude-desktop &
  ```
- **macOS / Windows**: Fully quit Claude from the dock or system tray (`Cmd+Q` / right-click tray &rarr; Quit) and reopen it.

##### ✅ Verifying the Connection:
1. Open Claude Desktop **Settings** (gear icon or `Ctrl+,` / `Cmd+,`).
2. In the left sidebar under **This computer**, click **Developer**.
3. You will see your server active:
   ```
   cv-compiler   [Running]
   Command:      /path/to/overleaf-cv-agent/.venv/bin/python
   Arguments:    /path/to/overleaf-cv-agent/server.py
   [View logs]
   ```
4. If it shows *"No servers added"*, an old instance was still running in the background; close it completely with `pkill -f claude-desktop` and restart.
5. You can click **View logs** at any time to verify the server status. In chats, you'll also see the 🔌 / 🔨 tool indicator confirming `compile_cv` is ready.

---

#### Option 2: Cursor IDE

1. Open **Cursor Settings** &rarr; **Features** &rarr; **MCP**.
2. Click **+ Add New MCP Server**.
3. Fill in:
   - **Name**: `cv-compiler`
   - **Type**: `command`
   - **Command**: `/absolute/path/to/overleaf-cv-agent/.venv/bin/python /absolute/path/to/overleaf-cv-agent/server.py`

---

#### Option 3: Windsurf IDE

Add to your `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "cv-compiler": {
      "command": "/absolute/path/to/overleaf-cv-agent/.venv/bin/python",
      "args": ["/absolute/path/to/overleaf-cv-agent/server.py"]
    }
  }
}
```

---

## 🎯 Day-to-Day Workflow

1. Open a new chat in your configured AI Project (e.g. Claude Project).
2. Paste the target Job Description:
   > *"Here is the job description for a Senior AI Agent Engineer at Anthropic. Tailor my CV and compile the PDF."*
3. The AI:
   - Analyzes requirements & extracts ATS keywords.
   - Reframes your actual experiences from `cv.tex` to emphasize target skills.
   - Formulates quantified STAR bullet points.
   - Automatically executes the `compile_cv` tool.
4. **Done!** Your compiled PDF appears in `out/` (e.g., `out/Your_Name_Your_Next_AI_Agent_Eng.pdf`).

---

## 💻 Standalone & CLI Usage

You can also use the compiler standalone without an AI assistant:

```bash
# Default: compiles local cv.tex
python main.py Agent_Dev

# Pipe LaTeX from terminal/stdin
cat cv.tex | python main.py Agent_Dev

# Pass a custom .tex file
python main.py Agent_Dev path/to/tailored.tex

# Pass raw LaTeX string
python main.py Agent_Dev "\documentclass{article}\begin{document}Hello\end{document}"
```

---

## 🐍 Python API Integration

```python
from main import generate_cv

# Pass raw LaTeX string directly
tailored_latex = r"""
\documentclass[11pt,a4paper]{article}
\begin{document}
...
\end{document}
"""

pdf_path = generate_cv(role="Agent_Dev", latex_source=tailored_latex)
print(f"Compiled PDF: {pdf_path}")
```

---

## 🧪 Running Automated Tests

A unit test suite is included to verify LaTeX extraction, PDF page-count validation, and filename formatting:

```bash
python3 -m unittest discover tests
```

---

## 🔒 Security Notice & Cookie Lifecycle

- **Session Confidentiality**: The `overleaf_session2` cookie grants access to your Overleaf account. Treat it like a password. Ensure `.env` is never committed (it is excluded by default in `.gitignore`).
- **Cookie Expiration**: Overleaf session cookies typically remain valid for several weeks/months. If compilation suddenly fails with an authentication error (`401` or `403`), simply log into Overleaf again, copy the fresh `overleaf_session2` cookie, and update your `.env` file.
- **Unofficial API**: Overleaf does not offer an official developer API for individual accounts; this tool interacts headlessly with Overleaf's web endpoints.

---

## 📂 Project Structure

```text
overleaf-cv-agent/
├── .env                         # Your private Overleaf credentials (git-ignored)
├── .env.example                 # Reference template for configuration
├── .gitignore                   # Keeps secrets, virtualenv, and PDFs safe
├── LICENSE                      # MIT License
├── cv.example.tex               # Public sample LaTeX template
├── cv.tex                       # Master LaTeX resume (git-ignored for privacy)
├── main.py                      # Core compiler library & CLI
├── server.py                    # FastMCP server for AI assistants
├── requirements.txt             # Python dependencies
├── PROJECT_INSTRUCTIONS.md      # Universal prompt template for AI Projects
├── README.md                    # Complete documentation
├── tests/                       # Unit tests
│   └── test_compiler.py
└── out/                         # Destination for generated PDFs (git-ignored)
    └── Candidate_Your_Next_Agent_Dev.pdf
```

---

## 🔗 Pair with Notion Job Tracker MCP

Supercharge your workflow by pairing **Overleaf CV Agent** with [Notion Job Tracker MCP](https://github.com/AhmedKhalifa3/notion-tracker-mcp):
1. **Compile:** Overleaf CV Agent compiles your tailored PDF resume in seconds.
2. **Auto-Log & Upload:** Notion Job Tracker automatically creates a card in your Notion applications board, categorizes the role, and uploads the generated PDF directly into the `CV` column.
3. **Track & Prep:** Calculate response rates, get stale application alerts, draft follow-up messages, and generate custom interview cheat sheets from your saved history.

---

## 📄 License

MIT License. Free to use and customize for your career search!
