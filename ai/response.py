"""
response.py

Defines the standard AI response model used throughout MAYDAY.

Every provider returns an AIResponse instance, providing a
consistent response interface across all AI providers.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class AIResponse:
    """
    Standard AI response model.
    """

    # ------------------------------------------------------------------
    # Required
    # ------------------------------------------------------------------

    content: str

    # ------------------------------------------------------------------
    # Provider Information
    # ------------------------------------------------------------------

    provider: str | None = None
    model: str | None = None

    # ------------------------------------------------------------------
    # Generation Information
    # ------------------------------------------------------------------

    finish_reason: str | None = None

    request_id: str | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    stream: bool = False

    # ------------------------------------------------------------------
    # Token Usage
    # ------------------------------------------------------------------

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)

    raw_response: dict[str, Any] = field(default_factory=dict)

    extra: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:

        if not self.content.strip():
            raise ValueError(
                "Response content cannot be empty."
            )

        if self.prompt_tokens < 0:
            raise ValueError(
                "prompt_tokens cannot be negative."
            )

        if self.completion_tokens < 0:
            raise ValueError(
                "completion_tokens cannot be negative."
            )

        if self.total_tokens < 0:
            raise ValueError(
                "total_tokens cannot be negative."
            )

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def copy(self, **changes: Any) -> "AIResponse":
        """
        Return a modified copy.
        """
        return replace(self, **changes)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert response into a dictionary.
        """
        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "AIResponse":
        """
        Create AIResponse from dictionary.
        """
        return cls(**data)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    @property
    def is_streaming(self) -> bool:
        return self.stream

    @property
    def token_usage(self) -> dict[str, int]:
        return {
            "prompt": self.prompt_tokens,
            "completion": self.completion_tokens,
            "total": self.total_tokens,
        }

    @property
    def has_raw_response(self) -> bool:
        return bool(self.raw_response)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"provider={self.provider!r}, "
            f"model={self.model!r}, "
            f"tokens={self.total_tokens}, "
            f"stream={self.stream}, "
            f"content_length={len(self.content)})"
        )