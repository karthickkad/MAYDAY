"""
prompts.py

Prompt management for MAYDAY.

Provides reusable prompt templates with variable substitution,
validation, and prompt management.
"""

from __future__ import annotations

from dataclasses import dataclass
from string import Formatter
from threading import RLock
from typing import Dict, Iterator


# ----------------------------------------------------------------------
# Prompt Template
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class PromptTemplate:
    """
    Represents a reusable prompt template.
    """

    name: str
    template: str
    description: str = ""

    def variables(self) -> tuple[str, ...]:
        """
        Return all required template variables.
        """

        variables = {
            field_name
            for _, field_name, _, _
            in Formatter().parse(self.template)
            if field_name
        }

        return tuple(sorted(variables))

    def render(self, **kwargs) -> str:
        """
        Render the prompt.

        Raises
        ------
        KeyError
            If one or more required variables are missing.
        """

        required = set(self.variables())

        missing = required.difference(kwargs.keys())

        if missing:
            raise KeyError(
                f"Missing template variables: {sorted(missing)}"
            )

        return self.template.format(**kwargs)

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}')"
        )


# ----------------------------------------------------------------------
# Prompt Manager
# ----------------------------------------------------------------------


class PromptManager:
    """
    Stores and manages reusable prompt templates.
    """

    def __init__(self) -> None:

        self._templates: Dict[str, PromptTemplate] = {}
        self._lock = RLock()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        template: PromptTemplate,
    ) -> None:
        """
        Register a prompt template.
        """

        key = template.name.lower()

        with self._lock:

            if key in self._templates:
                raise ValueError(
                    f"Prompt '{template.name}' already exists."
                )

            self._templates[key] = template

    # ------------------------------------------------------------------
    # Removal
    # ------------------------------------------------------------------

    def unregister(
        self,
        template_name: str,
    ) -> None:
        """
        Remove a prompt template.
        """

        key = template_name.lower()

        with self._lock:

            if key not in self._templates:
                raise KeyError(
                    f"Prompt '{template_name}' not found."
                )

            del self._templates[key]

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(
        self,
        template_name: str,
    ) -> PromptTemplate:
        """
        Return a prompt template.
        """

        key = template_name.lower()

        with self._lock:

            if key not in self._templates:
                raise KeyError(
                    f"Prompt '{template_name}' not found."
                )

            return self._templates[key]

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(
        self,
        template_name: str,
        **kwargs,
    ) -> str:
        """
        Render a registered prompt.
        """

        return self.get(template_name).render(**kwargs)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def exists(
        self,
        template_name: str,
    ) -> bool:

        with self._lock:
            return template_name.lower() in self._templates

    def list_templates(
        self,
    ) -> tuple[str, ...]:

        with self._lock:
            return tuple(
                sorted(self._templates.keys())
            )

    def clear(self) -> None:

        with self._lock:
            self._templates.clear()

    # ------------------------------------------------------------------
    # Python Special Methods
    # ------------------------------------------------------------------

    def __contains__(
        self,
        template_name: str,
    ) -> bool:

        return self.exists(template_name)

    def __len__(self) -> int:

        with self._lock:
            return len(self._templates)

    def __iter__(
        self,
    ) -> Iterator[PromptTemplate]:

        with self._lock:
            return iter(
                tuple(self._templates.values())
            )

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(templates={self.list_templates()})"
        )