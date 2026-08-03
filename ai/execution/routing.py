"""
routing.py

Provider routing module for MAYDAY.

Responsible for selecting the provider and model that will
execute an AI request.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ai.providers.base import BaseProvider
from ai.providers.manager import ProviderManager
from ai.request import AIRequest


# ----------------------------------------------------------------------
# Routing Result
# ----------------------------------------------------------------------


@dataclass(slots=True)
class RoutingResult:
    """
    Result returned by ProviderRouter.
    """

    provider: BaseProvider

    model: str

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def provider_name(self) -> str:
        """
        Return the selected provider name.
        """
        return self.provider.name

    def __bool__(self) -> bool:
        return self.provider is not None
    
    def route(
        self,
        request: AIRequest,
    ) -> RoutingResult:

        provider = self.select_provider(request)

        model = self.select_model(
            provider,
            request,
        )

        return RoutingResult(
            provider=provider,
            model=model,
            metadata={
                "default_provider": request.provider is None,
                "default_model": request.model is None,
            },
        )
        
# ----------------------------------------------------------------------
# Provider Router
# ----------------------------------------------------------------------


class ProviderRouter:
    """
    Routes AI requests to the appropriate provider and model.
    """

    def __init__(
        self,
        provider_manager: ProviderManager,
    ) -> None:
        self._provider_manager = provider_manager

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def route(
        self,
        request: AIRequest,
    ) -> RoutingResult:
        """
        Route an AI request to the appropriate provider and model.
        """

        provider = self.select_provider(request)

        model = self.select_model(
            provider,
            request,
        )

        return RoutingResult(
            provider=provider,
            model=model,
            metadata={
                "default_provider": request.provider is None,
                "default_model": request.model is None,
            },
        )
    # ------------------------------------------------------------------
    # Provider Selection
    # ------------------------------------------------------------------

    def select_provider(
        self,
        request: AIRequest,
    ) -> BaseProvider:
        """
        Select the provider that will execute the request.
        """

        if request.provider is None:
            return self.resolve_default_provider()

        provider = self._provider_manager.get(request.provider)

        return provider

    def resolve_default_provider(
        self,
    ) -> BaseProvider:
        """
        Return the default provider.
        """

        return self._provider_manager.default_provider()
    
    # ------------------------------------------------------------------
    # Model Selection
    # ------------------------------------------------------------------

    def select_model(
        self,
        provider: BaseProvider,
        request: AIRequest,
    ) -> str:
        """
        Select the model that will execute the request.
        """

        if request.model is None:
            return self.resolve_default_model(provider)

        if not self.supports_model(
            provider,
            request.model,
        ):
            raise ValueError(
                f"Provider '{provider.name}' "
                f"does not support model '{request.model}'."
            )

        return request.model

    def resolve_default_model(
        self,
        provider: BaseProvider,
    ) -> str:
        """
        Return the provider's default model.
        """

        return provider.default_model()

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def supports_model(
        self,
        provider: BaseProvider,
        model: str,
    ) -> bool:
        """
        Check whether a provider supports a model.
        """

        return provider.supports_model(model)

    # ------------------------------------------------------------------
    # Python Methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Return the string representation of the router.
        """

        return (
            f"{self.__class__.__name__}"
            f"(providers={len(self._provider_manager)})"
        )
