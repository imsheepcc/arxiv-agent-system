"""
Command execution tools for agents (restricted to the output directory).
"""

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class _RunCommandResult:
    exit_code: int
    stdout: str
    stderr: str


class CommandTools:
    """Restricted command execution tools for agents."""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
        self.base_dir = os.path.abspath(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)

        self._allowed_commands = {
            "python",
            "python3",
            "py",
            "node",
            "npm",
            "npx",
        }

    def run_command(self, command: str, args: Optional[List[str]] = None, timeout_seconds: int = 20) -> Dict[str, Any]:
        """Run a restricted command inside the output directory."""

        if not command or not isinstance(command, str):
            return {"status": "error", "message": "Command must be a non-empty string"}

        cmd_lower = command.strip().lower()
        if cmd_lower not in self._allowed_commands:
            return {
                "status": "error",
                "message": f"Command not allowed: {command}. Allowed: {sorted(self._allowed_commands)}",
            }

        args = args or []
        if not isinstance(args, list) or any(not isinstance(a, str) for a in args):
            return {"status": "error", "message": "Args must be a list of strings"}

        for a in args:
            a_stripped = a.strip()
            if not a_stripped:
                continue
            if ".." in a_stripped:
                return {"status": "error", "message": "Path traversal in args is not allowed"}
            if os.path.isabs(a_stripped):
                return {"status": "error", "message": "Absolute paths in args are not allowed"}
            if ":" in a_stripped:
                return {"status": "error", "message": "Drive paths in args are not allowed"}

        try:
            completed = subprocess.run(
                [command] + args,
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=max(1, int(timeout_seconds)),
                shell=False,
            )

            result = _RunCommandResult(
                exit_code=int(completed.returncode),
                stdout=completed.stdout or "",
                stderr=completed.stderr or "",
            )

            return {
                "status": "success" if result.exit_code == 0 else "error",
                "message": "Command executed" if result.exit_code == 0 else f"Command failed with exit code {result.exit_code}",
                "exit_code": result.exit_code,
                "stdout": result.stdout[:8000],
                "stderr": result.stderr[:8000],
            }

        except subprocess.TimeoutExpired:
            return {"status": "error", "message": f"Command timed out after {timeout_seconds}s"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to run command: {str(e)}"}

    def run_tests(self) -> Dict[str, Any]:
        """Run basic, safe checks against the generated static website in outputs/."""

        required_files = [
            "index.html",
            "category.html",
            "paper.html",
            os.path.join("css", "style.css"),
            os.path.join("js", "script.js"),
            os.path.join("data", "papers.json"),
        ]

        checks: List[Dict[str, Any]] = []

        def _check(name: str, passed: bool, detail: str = ""):
            checks.append({"name": name, "passed": bool(passed), "detail": detail})

        # Existence checks
        for rel_path in required_files:
            full_path = os.path.join(self.base_dir, rel_path)
            _check(f"file_exists:{rel_path}", os.path.exists(full_path), full_path)

        # Validate papers.json
        papers_json_path = os.path.join(self.base_dir, "data", "papers.json")
        if os.path.exists(papers_json_path):
            try:
                with open(papers_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                has_papers = isinstance(data.get("papers"), list) and len(data.get("papers", [])) > 0
                has_categories = isinstance(data.get("categories"), dict) and len(data.get("categories", {})) > 0
                _check("papers_json:has_papers", has_papers)
                _check("papers_json:has_categories", has_categories)
            except Exception as e:
                _check("papers_json:valid_json", False, str(e))
        else:
            _check("papers_json:present", False, papers_json_path)

        # HTML structure checks
        def _read_text(rel_path: str) -> str:
            p = os.path.join(self.base_dir, rel_path)
            with open(p, "r", encoding="utf-8") as f:
                return f.read()

        try:
            paper_html = _read_text("paper.html")
            _check("paper_html:has_bibtex_container", "bibtexCitation" in paper_html)
            _check("paper_html:has_standard_container", "standardCitation" in paper_html)
            _check("paper_html:has_copy_buttons", "copyCitation('bibtex')" in paper_html and "copyCitation('standard')" in paper_html)
        except Exception as e:
            _check("paper_html:readable", False, str(e))

        try:
            script_js = _read_text(os.path.join("js", "script.js"))
            _check("script_js:has_loadCategories", "function loadCategories" in script_js)
            _check("script_js:has_loadPapers", "function loadPapers" in script_js)
            _check("script_js:has_loadPaperDetails", "function loadPaperDetails" in script_js)
            _check("script_js:has_copyCitation", "function copyCitation" in script_js)
        except Exception as e:
            _check("script_js:readable", False, str(e))

        passed = all(c["passed"] for c in checks) if checks else False
        return {"status": "success" if passed else "error", "passed": passed, "checks": checks}

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get tool definitions in OpenAI function calling format."""

        return [
            {
                "type": "function",
                "function": {
                    "name": "run_command",
                    "description": "Run a restricted command inside the generated project's output directory (outputs/).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Command to run (allowlisted).",
                            },
                            "args": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Command arguments (no absolute paths).",
                            },
                            "timeout_seconds": {
                                "type": "integer",
                                "description": "Timeout in seconds (default 20).",
                                "minimum": 1,
                                "maximum": 120,
                            },
                        },
                        "required": ["command"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "run_tests",
                    "description": "Run safe, basic checks against the generated static website files in outputs/.",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
        ]
