# MAYDAY API Reference

> Public API documentation for the MAYDAY AI Framework.

---

## Overview

MAYDAY provides a unified API for interacting with multiple AI providers through a consistent interface.

The framework abstracts provider-specific implementations and exposes a provider-independent programming model.

---

## Package Structure

```text
ai/
├── request.py
├── response.py
├── session.py
├── prompts.py
├── engine.py
├── events.py
├── exceptions.py
├── execution/
└── providers/
```

---

## Core Classes

### Request

Represents an AI request.

Responsibilities

- Prompt
- Model
- Provider
- Parameters
- Options

Example

```python
from ai.request import Request

request = Request(
    prompt="Hello, MAYDAY!"
)
```

---

### Response

Represents the response returned by an AI provider.

Responsibilities

- Generated content
- Provider information
- Model information
- Usage statistics
- Metadata

Example

```python
response = provider.generate(request)

print(response.content)
```

---

### Session

Maintains conversational state.

Responsibilities

- Conversation history
- Context management
- Session metadata

Example

```python
session = Session()

session.add_user_message("Hello")

session.add_assistant_message("Hi!")
```

---

### Prompt

Represents prompt templates and prompt utilities.

Responsibilities

- Prompt construction
- Prompt formatting
- Template management

---

## Provider API

### BaseProvider

Every provider implements the same interface.

Example

```python
provider.generate(request)

provider.models()

provider.health()

provider.info()
```

---

## Provider Manager

Responsible for selecting and managing providers.

Example

```python
manager = ProviderManager()

provider = manager.get("openai")
```

---

## Registry API

Register a provider

```python
registry.register(provider)
```

Lookup

```python
registry.get("openai")
```

List providers

```python
registry.providers()
```

---

## Factory API

Create provider

```python
provider = factory.create("openai")
```

---

## Execution API

Execute request

```python
executor.execute(request)
```

Validate request

```python
validator.validate(request)
```

Route request

```python
routing.route(request)
```

Run pipeline

```python
pipeline.execute(request)
```

---

## Exceptions

Framework exceptions

- MaydayError
- ValidationError
- ProviderError
- ConfigurationError
- ExecutionError

Provider exceptions

- ProviderNotFoundError
- ProviderUnavailableError
- ProviderAuthenticationError

---

## Configuration

Example

```python
provider = factory.create(
    "openai",
    api_key="YOUR_API_KEY",
)
```

---

## Typical Usage

```python
from ai.request import Request
from ai.providers.factory import ProviderFactory

provider = ProviderFactory.create(
    "openai",
)

request = Request(
    prompt="Explain recursion."
)

response = provider.generate(
    request,
)

print(response.content)
```

---

## Supported Providers

- OpenAI
- Ollama
- Gemini
- Anthropic
- Groq
- OpenRouter
- DeepSeek
- Cohere
- Mistral
- LM Studio
- xAI

---

## Future API

Planned additions

- Streaming API
- Embedding API
- Vision API
- Audio API
- Tool Calling API
- Batch API
- Async API

---

## Versioning

API changes follow the MAYDAY release version.

Current version format

```text
Vyyyy.mm.dd.build
```

Example

```text
V2026.08.03.001
```

---

## Related Documents

- architecture.md
- execution.md
- providers.md
- roadmap.md
