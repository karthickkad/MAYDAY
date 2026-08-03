# MAYDAY Roadmap

> Long-term development roadmap for the MAYDAY AI Framework.

---

## Current Status

### Framework Foundation

### AI Core

- [x] request.py
- [x] response.py
- [x] session.py
- [x] prompts.py
- [x] exceptions.py
- [ ] engine.py
- [ ] events.py
- [ ] ai/utils.py

### Execution Framework

- [x] executor.py
- [x] pipeline.py
- [x] routing.py
- [x] validator.py
- [ ] middleware.py

### Provider Framework

- [x] base.py
- [x] registry.py
- [x] factory.py
- [x] manager.py
- [x] provider_info.py
- [x] capabilities.py
- [x] health.py
- [x] exceptions.py

### Provider Implementations

- [ ] OpenAI
- [ ] Ollama
- [ ] Gemini
- [ ] Anthropic
- [ ] Groq
- [ ] OpenRouter
- [ ] DeepSeek
- [ ] Cohere
- [ ] Mistral
- [ ] LM Studio
- [ ] xAI
- [ ] Dummy
- [ ] Mock

### Infrastructure Status

- [ ] Cache
- [ ] Metrics
- [ ] Models
- [ ] Security
- [ ] AI Utilities

---

## Next Milestone

### Goal

Complete the framework foundation.

### Remaining Modules

- [ ] middleware.py
- [ ] engine.py
- [ ] events.py
- [ ] ai/utils.py

---

## Upcoming Milestones

### Provider Integrations

Priority

- OpenAI
- Ollama
- Dummy
- Mock

Secondary

- Gemini
- Anthropic
- Groq
- DeepSeek
- OpenRouter
- Mistral
- Cohere
- LM Studio
- xAI

---

### Infrastructure

- Cache Layer
- Metrics Collection
- Security Layer
- Data Models

---

### Advanced Features

- Streaming Responses
- Function Calling
- Vision Models
- Audio Models
- Embeddings
- Conversation Memory
- Plugin Architecture
- Automatic Failover
- Load Balancing
- Circuit Breaker
- Retry Policies

---

### Developer Experience

- CLI Improvements
- Release Automation
- Documentation Automation
- CI/CD
- Coverage Reports
- Performance Benchmarks

---

## Future Vision

MAYDAY aims to become a production-ready, provider-agnostic AI framework with:

- Unified provider interface
- Modular execution pipeline
- Intelligent provider routing
- High test coverage
- Automated release workflow
- Comprehensive documentation
- Enterprise-ready architecture

---

## Development Principles

- Build the framework before provider implementations.
- Keep modules independent and reusable.
- Every feature must include tests.
- Documentation is updated with every milestone.
- Maintain consistent coding standards.

---

## Versioning

MAYDAY follows the custom version format:

Vyyyy.mm.dd.build

Example:

V2026.08.03.001

---

## Project Health

Framework Foundation      ████████████░░░░ 80%

Execution Framework       ███████████░░░░░ 80%

Provider Framework        ████████████████ 100%

Provider Implementations  ░░░░░░░░░░░░░░░░ 0%

Infrastructure            ░░░░░░░░░░░░░░░░ 0%

Documentation             ████████░░░░░░░░ 50%

Testing                   ███████████░░░░░ 75%
