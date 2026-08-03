# MAYDAY Architecture

> High-level architecture of the MAYDAY AI Framework.

---

## Overview

MAYDAY is a modular, provider-agnostic AI framework designed to provide a unified interface for interacting with multiple Large Language Model (LLM) providers.

The framework separates responsibilities into independent modules to improve maintainability, extensibility, and testability.

---

## Architecture Principles

- Modular design
- Provider abstraction
- Separation of concerns
- Immutable data models
- Test-driven development
- Extensible provider framework
- Provider independence

---

## High-Level Architecture

                        User
                         │
                         ▼
                    AI Request
                         │
                         ▼
                    Validator
                         │
                         ▼
                   Middleware
                         │
                         ▼
                     Pipeline
                         │
                         ▼
                     Routing
                         │
                         ▼
                Provider Manager
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          OpenAI      Ollama     Gemini
              │          │          │
              └──────────┼──────────┘
                         ▼
                    AI Response
                         │
                         ▼
                       User

---

## Package Architecture

ai/

├── execution/
│   ├── executor.py
│   ├── middleware.py
│   ├── pipeline.py
│   ├── routing.py
│   └── validator.py
│
├── providers/
│   ├── base.py
│   ├── registry.py
│   ├── manager.py
│   ├── factory.py
│   ├── provider_info.py
│   ├── capabilities.py
│   ├── health.py
│   └── implementations
│
├── cache/
├── metrics/
├── security/
├── models/
└── utils/

---

## AI Request Flow

1. User creates a Request.
2. Validator validates the request.
3. Middleware applies preprocessing.
4. Pipeline executes processing stages.
5. Routing selects the provider.
6. Provider Manager obtains the provider.
7. Provider executes the request.
8. Response is returned to the user.

---

## Provider Framework

The provider framework consists of:

- Base Provider
- Provider Registry
- Provider Factory
- Provider Manager
- Provider Information
- Provider Health
- Provider Capabilities

These components allow providers to be added without changing the framework.

---

## Execution Framework

Execution is divided into independent stages.

Request

↓

Validator

↓

Middleware

↓

Pipeline

↓

Routing

↓

Provider

↓

Response

---

## Core Components

### Request

Represents an AI request.

### Response

Represents the provider response.

### Session

Maintains conversational state.

### Prompts

Prompt management.

### Exceptions

Framework-wide exception hierarchy.

---

## Future Components

- Cache
- Metrics
- Security
- Models
- Event System
- AI Engine

---

## Design Goals

- Provider agnostic
- High performance
- Easy to extend
- Fully testable
- Clear separation of concerns
- Production ready

---

## Dependencies

User

↓

AI Core

↓

Execution Layer

↓

Provider Framework

↓

Provider Implementation

↓

External AI Provider

---

## Project Status

The architecture is designed so that new providers and execution features can be added without modifying the existing framework.

This enables long-term scalability while maintaining a consistent developer experience.
