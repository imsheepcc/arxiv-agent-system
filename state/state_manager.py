"""Persisted state and memory management for the multi-agent system."""

import json
import os
from copy import deepcopy
from typing import Any, Dict, List, Optional

from agents.base_agent import BaseAgent


class StateManager:
    """Handles saving/loading project state and agent memories."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.state = self._load()

    def _default_state(self) -> Dict[str, Any]:
        return {
            "project_plan": None,
            "completed_tasks": [],
            "created_files": [],
            "task_results": {},
            "evaluation": None,
            "agents": {},
            "last_updated": None,
        }

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                default_state = self._default_state()
                default_state.update(data)
                return default_state
            except Exception:
                # Fallback to default state if corrupted
                return self._default_state()
        return self._default_state()

    def _save(self) -> None:
        temp_path = f"{self.file_path}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, self.file_path)

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if key in {"completed_tasks", "created_files"} and value is not None:
                self.state[key] = list(value)
            elif key in {"task_results", "project_plan", "evaluation"}:
                self.state[key] = deepcopy(value)
            else:
                self.state[key] = value
        self.state["last_updated"] = self._current_timestamp()
        self._save()

    def record_agent_memory(self, agent: BaseAgent) -> None:
        if not isinstance(agent, BaseAgent):
            return
        if "agents" not in self.state:
            self.state["agents"] = {}
        self.state["agents"][agent.role] = agent.export_memory()
        self.state["last_updated"] = self._current_timestamp()
        self._save()

    def restore_agent_memory(self, agent: BaseAgent) -> None:
        if not isinstance(agent, BaseAgent):
            return
        memory = self.state.get("agents", {}).get(agent.role)
        if memory:
            agent.load_memory(memory)

    def get_recent_tasks(self, limit: int = 5) -> List[Any]:
        return list(self.state.get("completed_tasks", [])[-limit:])

    def get_recent_files(self, limit: int = 5) -> List[str]:
        return list(self.state.get("created_files", [])[-limit:])

    def get_agent_memory(self, role: str) -> Optional[Dict[str, Any]]:
        return deepcopy(self.state.get("agents", {}).get(role))

    def _current_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat() + "Z"
