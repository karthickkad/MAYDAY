"""
base.py

Abstract base class for all AI providers supported by MAYDAY.

Every provider (OpenAI, Ollama, Gemini, Anthropic, etc.) must inherit from
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
        Return the provider name.

        Example:
            OpenAI
            Ollama
            Gemini
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Return the provider implementation version.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize provider resources.

        Returns:
            True if initialization succeeds.
        """
        raise NotImplementedError

    @abstractmethod
    def shutdown(self) -> None:
        """
        Release provider resources.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Chat Completion
    # ------------------------------------------------------------------

    @abstractmethod
    def generate(
        self,
        prompt: str,
        model: str,
        **kwargs: Any,
    ) -> Any:
        """
        Generate a standard (non-streaming) response.
        """
        raise NotImplementedError

    @abstractmethod
    def stream(
        self,
        prompt: str,
        model: str,
        **kwargs: Any,
    ) -> Iterator[Any]:
        """
        Generate a streaming response.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Model Management
    # ------------------------------------------------------------------

    @abstractmethod
    def list_models(self) -> list[str]:
        """
        Return all supported models.
        """
        raise NotImplementedError

    @abstractmethod
    def default_model(self) -> str:
        """
        Return the default model.
        """
        raise NotImplementedError

    @abstractmethod
    def supports_model(self, model: str) -> bool:
        """
        Check whether the specified model is supported.

        Args:
            model: Model name.

        Returns:
            True if the model is supported.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Health & Configuration
    # ------------------------------------------------------------------

    @abstractmethod
    def health_check(self) -> bool:
        """
        Verify provider connectivity.

        Returns:
            True if the provider is healthy.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate provider configuration.

        Returns:
            True if the configuration is valid.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Provider Metadata
    # ------------------------------------------------------------------

    @abstractmethod
    def provider_info(self) -> dict[str, Any]:
        """
        Return provider metadata.

        Example:
        {
            "name": "OpenAI",
            "version": "1.0",
            "supports_streaming": True
        }
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """
        Return whether the provider supports streaming.
        """
        raise NotImplementedError