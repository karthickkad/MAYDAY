"""
session.py

Conversation session management for MAYDAY.

A session stores the complete history of AIRequest and AIResponse
objects exchanged during a conversation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any

from ai.request import AIRequest
from ai.response import AIResponse


# ----------------------------------------------------------------------
# Conversation Turn
# ----------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class ConversationTurn:
    """
    Represents one request/response interaction.
    """

    request: AIRequest
    response: AIResponse

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ----------------------------------------------------------------------
# Session
# ----------------------------------------------------------------------

@dataclass(slots=True)
class AISession:
    """
    Represents a conversation session.
    """

    session_id: str = field(default_factory=lambda: str(uuid4()))

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    metadata: dict[str, Any] = field(default_factory=dict)

    turns: list[ConversationTurn] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Conversation
    # ------------------------------------------------------------------

    def add(
        self,
        request: AIRequest,
        response: AIResponse,
    ) -> None:
        """
        Add a conversation turn.
        """
        self.turns.append(
            ConversationTurn(
                request=request,
                response=response,
            )
        )

        self.updated_at = datetime.now(timezone.utc)

    # ------------------------------------------------------------------
    # Access
    # ------------------------------------------------------------------

    def last_request(self) -> AIRequest | None:
        """
        Return the last request.
        """
        if not self.turns:
            return None

        return self.turns[-1].request

    def last_response(self) -> AIResponse | None:
        """
        Return the last response.
        """
        if not self.turns:
            return None

        return self.turns[-1].response

    def history(self) -> tuple[ConversationTurn, ...]:
        """
        Return conversation history.
        """
        return tuple(self.turns)

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def turn_count(self) -> int:
        return len(self.turns)

    @property
    def total_tokens(self) -> int:
        return sum(
            turn.response.total_tokens
            for turn in self.turns
        )

    # ------------------------------------------------------------------
    # Management
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """
        Clear conversation history.
        """
        self.turns.clear()
        self.updated_at = datetime.now(timezone.utc)

    def copy(self) -> "AISession":
        """
        Return a copy of the session.
        """
        return replace(
            self,
            metadata=self.metadata.copy(),
            turns=self.turns.copy(),
        )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize session.
        """
        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "AISession":
        """
        Restore a session.

        Note:
            Nested AIRequest/AIResponse restoration
            will be implemented in a future version.
        """
        return cls(
            session_id=data["session_id"],
            metadata=data.get("metadata", {}),
        )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id='{self.session_id}', "
            f"turns={self.turn_count})"
        )