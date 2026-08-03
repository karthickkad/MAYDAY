"""
validator.py

Validation module for MAYDAY.

Responsible for validating AI requests before execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ai.prompts import PromptManager
from ai.providers.manager import ProviderManager
from ai.request import AIRequest
from ai.providers.base import BaseProvider

# ----------------------------------------------------------------------
# Validation Result
# ----------------------------------------------------------------------


@dataclass(slots=True)
class ValidationResult:
    """
    Result returned by RequestValidator.
    """

    valid: bool = True

    errors: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    def add_error(self, message: str) -> None:
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)

    # ------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------

    @property
    def error_count(self) -> int:
        """
        Return the number of validation errors.
        """
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        """
        Return the number of validation warnings.
        """
        return len(self.warnings)

    def __bool__(self) -> bool:
        return self.valid

# ----------------------------------------------------------------------
# Request Validator
# ----------------------------------------------------------------------


class RequestValidator:
    """
    Validates AIRequest objects.
    """

    def __init__(
        self,
        provider_manager: ProviderManager,
        prompt_manager: PromptManager | None = None,
    ) -> None:

        self._provider_manager = provider_manager
        self._prompt_manager = prompt_manager
    
    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    def _get_provider(
        self,
        provider_name: str,
    ) -> BaseProvider | None:
        """
        Safely retrieve a provider.

        Returns
        -------
        BaseProvider | None
            Provider instance if registered, otherwise None.
        """
        if not self._provider_manager.exists(provider_name):
            return None

        return self._provider_manager.get(provider_name)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate(
        self,
        request: AIRequest,
    ) -> ValidationResult:
        """
        Perform complete validation.
        """

        result = ValidationResult()

        self.validate_request(request, result)
        self.validate_provider(request, result)
        self.validate_model(request, result)
        self.validate_parameters(request, result)
        self.validate_stream(request, result)
        self.validate_prompt(request, result)

        return result

    # ------------------------------------------------------------------
    # Request
    # ------------------------------------------------------------------

    def validate_request(
        self,
        request: AIRequest,
        result: ValidationResult,
    ) -> None:

        if not request.prompt or not request.prompt.strip():
            result.add_error("Prompt cannot be empty.")

    # ------------------------------------------------------------------
    # Provider
    # ------------------------------------------------------------------

    def validate_provider(
        self,
        request: AIRequest,
        result: ValidationResult,
    ) -> None:

        if request.provider is None:
            result.add_warning(
                "No provider specified. Default provider will be used."
            )
            return

        provider = self._get_provider(request.provider)

        if provider is None:
            result.add_error(
                f"Unknown provider: '{request.provider}'."
            )
            return

        if not provider.health_check():
            result.add_error(
                f"Provider '{request.provider}' is unavailable."
            )

    # ------------------------------------------------------------------
    # Model
    # ------------------------------------------------------------------

    def validate_model(
        self,
        request: AIRequest,
        result: ValidationResult,
    ) -> None:

        if request.provider is None:
            return

        if request.model is None:
            result.add_warning(
                "No model specified. Default model will be used."
            )
            return

        provider = self._get_provider(request.provider)
        
        if provider is None:
            return

        if not provider.supports_model(request.model):
            result.add_error(
                f"Provider '{request.provider}' "
                f"does not support model '{request.model}'."
            )

    # ------------------------------------------------------------------
    # Parameters
    # ------------------------------------------------------------------

    def validate_parameters(
        self,
        request: AIRequest,
        result: ValidationResult,
    ) -> None:

        if not (0.0 <= request.temperature <= 2.0):
            result.add_error(
                "temperature must be between 0.0 and 2.0."
            )

        if not (0.0 <= request.top_p <= 1.0):
            result.add_error(
                "top_p must be between 0.0 and 1.0."
            )

        if request.max_tokens is not None:

            if request.max_tokens <= 0:
                result.add_error(
                    "max_tokens must be greater than zero."
                )

    # ------------------------------------------------------------------
    # Streaming
    # ------------------------------------------------------------------

    def validate_stream(
        self,
        request: AIRequest,
        result: ValidationResult,
    ) -> None:

        if not request.stream:
            return

        if request.provider is None:
            return

        provider = self._get_provider(request.provider)
        
        if provider is None:
            return

        if not provider.supports_streaming():
            result.add_error(
                f"Provider '{request.provider}' "
                "does not support streaming."
            )

    # ------------------------------------------------------------------
    # Prompt
    # ------------------------------------------------------------------

    def validate_prompt(
        self,
        request: AIRequest,
        result: ValidationResult,
    ) -> None:
        """
        Reserved for PromptManager integration.

        Future versions will validate prompt templates
        and template variables here.
        """

        if self._prompt_manager is None:
            return

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def validate_or_raise(
        self,
        request: AIRequest,
    ) -> None:

        result = self.validate(request)

        if result.has_errors:
            raise ValueError(
                "\n".join(result.errors)
            )