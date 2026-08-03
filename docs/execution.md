# MAYDAY Provider Framework

> This document describes the provider architecture used by the MAYDAY AI Framework.

---

## Overview

The Provider Framework enables MAYDAY to communicate with multiple AI providers through a unified interface.

Its primary goals are:

- Provider independence
- Easy extensibility
- Unified API
- Runtime provider selection
- Health monitoring
- Capability discovery

---

## Provider Architecture

```text
                    AI Request
                         │
                         ▼
                Provider Manager
                         │
                         ▼
                Provider Registry
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
        OpenAI      Anthropic      Ollama
            │            │            │
            └────────────┼────────────┘
                         ▼
                   AI Response
```

---

## Package Structure

```text
ai/
└── providers/
    ├── base.py
    ├── registry.py
    ├── factory.py
    ├── manager.py
    ├── provider_info.py
    ├── capabilities.py
    ├── health.py
    ├── exceptions.py
    ├── openai.py
    ├── ollama.py
    ├── gemini.py
    ├── anthropic.py
    └── ...
```

---

## Framework Components

### Base Provider

Defines the common interface implemented by every provider.

Responsibilities:

- Standard provider API
- Request execution
- Model listing
- Validation
- Authentication

---

### Provider Registry

Maintains the list of available providers.

Responsibilities:

- Register providers
- Remove providers
- Lookup providers
- Enumerate providers

---

### Provider Factory

Creates provider instances.

Responsibilities:

- Object creation
- Configuration
- Dependency injection
- Provider initialization

---

### Provider Manager

Coordinates provider usage.

Responsibilities:

- Provider selection
- Health checks
- Availability checks
- Lifecycle management

---

### Provider Information

Stores provider metadata.

Examples:

- Name
- Display name
- Version
- Supported models
- Capabilities
- Priority

---

### Provider Capabilities

Describes supported features.

Examples:

- Chat
- Vision
- Audio
- Embeddings
- Tool Calling
- Streaming

---

### Provider Health

Tracks runtime health.

Examples:

- Availability
- Status
- Latency
- Success rate
- Retry count
- Failure count

---

### Provider Exceptions

Defines provider-specific exception hierarchy.

Examples:

- ProviderNotFoundError
- ProviderUnavailableError
- ProviderConfigurationError
- ProviderAuthenticationError

---

## Provider Lifecycle

```text
Create

↓

Configure

↓

Register

↓

Validate

↓

Health Check

↓

Execute Request

↓

Return Response

↓

Shutdown
```

---

## Provider Selection

Provider selection may consider:

- Requested provider
- Provider availability
- Health status
- Supported capabilities
- Priority
- Default provider

Future enhancements may include:

- Cost-based routing
- Load balancing
- Geographic routing
- Automatic failover

---

## Adding a New Provider

1. Create a provider implementation.
2. Inherit from `BaseProvider`.
3. Implement required methods.
4. Register the provider.
5. Add unit tests.
6. Update documentation.

---

## Supported Providers

### Planned

- OpenAI
- Ollama
- Gemini
- Anthropic
- Groq
- OpenRouter
- DeepSeek
- Mistral
- Cohere
- LM Studio
- xAI

---

## Future Enhancements

- Dynamic provider discovery
- Plugin support
- Provider marketplace
- Hot reloading
- Automatic failover
- Load balancing
- Multi-provider execution
- Provider benchmarking

---

## Design Principles

- Provider agnostic
- Modular
- Extensible
- Testable
- Thread-safe
- Production ready

---

## Related Documents

- architecture.md
- execution.md
- api.md
- roadmap.md
