"""Unified agent communication message schema."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict


class MessageType(Enum):
    """Supported message categories for agent coordination."""

    PLAN_REQUEST = "plan_request"
    PLAN_RESPONSE = "plan_response"
    TASK_ASSIGNMENT = "task_assignment"
    TASK_RESULT = "task_result"
    EVAL_REQUEST = "evaluation_request"
    EVAL_REPORT = "evaluation_report"


@dataclass
class AgentMessage:
    """Standardized payload exchanged among orchestrator and agents."""

    id: str
    msg_type: MessageType
    sender: str
    receiver: str
    payload: Dict[str, Any]
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize message to dict (with enum converted to value)."""
        data = asdict(self)
        data["msg_type"] = self.msg_type.value
        return data

    def to_json(self, pretty: bool = True) -> str:
        """Serialize message to JSON string for LLM prompts/logs."""
        if pretty:
            return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        """Reconstruct AgentMessage from serialized dict."""
        return cls(
            id=data["id"],
            msg_type=MessageType(data["msg_type"]),
            sender=data["sender"],
            receiver=data["receiver"],
            payload=data.get("payload", {}),
            timestamp=data["timestamp"],
        )

    @classmethod
    def create(
        cls,
        msg_type: MessageType,
        sender: str,
        receiver: str,
        payload: Dict[str, Any],
    ) -> "AgentMessage":
        """Convenience factory with generated id/timestamp."""
        return cls(
            id=str(uuid.uuid4()),
            msg_type=msg_type,
            sender=sender,
            receiver=receiver,
            payload=payload,
            timestamp=datetime.utcnow().isoformat() + "Z",
        )
