"""
base.py

Abstract base class for all AI providers supported by MAYDAY.

Every provider (OpenAI, Ollama, Gemini, Claude, etc.) must inherit from
BaseProvider and implement every abstract method defined here.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterator


class BaseProvider(ABC):
    """
    Abstract interface for all MAYDAY AI providers.
    """

    # ------------------------------------------------------------------
    # Provider Information
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Provider name.

        Example:
            OpenAI
            Ollama
            Gemini
        """
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Provider implementation version.
        """
        pass

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize provider resources.
        """
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """
        Release provider resources.
        """
        pass

    # ------------------------------------------------------------------
    # Chat Completion
    # ------------------------------------------------------------------

    @abstractmethod
    def generate(
        self,
        prompt: str,
        model: str,
        **kwargs: Any
    ) -> Any:
        """
        Generate a standard (non-streaming) response.
        """
        pass

    @abstractmethod
    def stream(
        self,
        prompt: str,
        model: str,
        **kwargs: Any
    ) -> Iterator[Any]:
        """
        Generate a streaming response.
        """
        pass

    # ------------------------------------------------------------------
    # Model Management
    # ------------------------------------------------------------------

    @abstractmethod
    def list_models(self) -> list[str]:
        """
        Return all supported models.
        """
        pass

    @abstractmethod
    def default_model(self) -> str:
        """
        Return the default model.
        """
        pass

    @abstractmethod
    def supports_model(self, model: str) -> bool:
        """
        Check whether a model is supported.
        """
        pass

    # ------------------------------------------------------------------
    # Health & Configuration
    # ------------------------------------------------------------------

    @abstractmethod
    def health_check(self) -> bool:
        """
        Verify provider connectivity.
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate provider configuration.
        """
        pass

    # ------------------------------------------------------------------
    # Provider Information
    # ------------------------------------------------------------------

    @abstractmethod
    def provider_info(self) -> dict[str, Any]:
        """
        Return provider metadata.
        """
        pass

    @abstractmethod
    def supports_streaming(self) -> bool:
        """
        Return whether streaming is supported.
        """
        pass