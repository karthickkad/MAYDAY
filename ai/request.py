"""
request.py

Defines the standard AI request model used throughout MAYDAY.

Every provider accepts an AIRequest instance rather than individual
arguments, providing a consistent interface across all AI providers.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from typing import Any


@dataclass(frozen=True, slots=True)
class AIRequest:
    """
    Standard AI request model.

    This object represents a single request sent to an AI provider.
    """

    # ------------------------------------------------------------------
    # Required
    # ------------------------------------------------------------------

    prompt: str

    # ------------------------------------------------------------------
    # Provider
    # ------------------------------------------------------------------

    provider: str | None = None
    model: str | None = None

    # ------------------------------------------------------------------
    # Prompt Configuration
    # ------------------------------------------------------------------

    system_prompt: str | None = None

    # ------------------------------------------------------------------
    # Generation Parameters
    # ------------------------------------------------------------------

    temperature: float = 0.7
    max_tokens: int | None = None
    top_p: float = 1.0

    stream: bool = False

    stop: tuple[str, ...] = field(default_factory=tuple)

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)

    extra: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:

        if not self.prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        if not (0.0 <= self.temperature <= 2.0):
            raise ValueError(
                "temperature must be between 0.0 and 2.0."
            )

        if not (0.0 <= self.top_p <= 1.0):
            raise ValueError(
                "top_p must be between 0.0 and 1.0."
            )

        if self.max_tokens is not None:
            if self.max_tokens <= 0:
                raise ValueError(
                    "max_tokens must be greater than zero."
                )

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def copy(self, **changes: Any) -> "AIRequest":
        """
        Return a modified copy of the request.
        """
        return replace(self, **changes)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert request into a dictionary.
        """
        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "AIRequest":
        """
        Construct AIRequest from a dictionary.
        """
        return cls(**data)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def has_system_prompt(self) -> bool:
        """
        Whether a system prompt exists.
        """
        return bool(self.system_prompt)

    @property
    def is_streaming(self) -> bool:
        """
        Whether streaming is enabled.
        """
        return self.stream

    @property
    def has_metadata(self) -> bool:
        """
        Whether metadata is attached.
        """
        return bool(self.metadata)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"provider={self.provider!r}, "
            f"model={self.model!r}, "
            f"stream={self.stream}, "
            f"prompt_length={len(self.prompt)})"
        )