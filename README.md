# MAYDAY

> **A Modular Python Framework for AI, Automation, and Embedded Systems Development**

MAYDAY is an open-source, modular Python framework designed to build scalable AI assistants, automation tools, and embedded firmware testing solutions. The project follows professional software engineering practices with a strong emphasis on modularity, maintainability, extensibility, and automated development workflows.

Layer 1 establishes the foundation of the project by providing a structured architecture, automated release management, version control integration, and comprehensive testing.

---

## Features

* Modular project architecture
* Configuration management using JSON
* Command management framework
* Built-in logging system
* Custom exception handling
* Utility helper functions
* Automated unit testing
* Automated Release Manager
* Automatic version management
* Automatic README updates
* Automatic CHANGELOG updates
* Git integration
* GitHub Release integration (GitHub CLI)
* Extensible architecture for future modules

---

## Current Version

| Property | Value                |
| -------- | -------------------- |
| Version  | **2026.07.26.8**     |
| Status   | **Layer 1 Complete** |

> **Note:** The version number is automatically updated by the Release Manager.

---

## Requirements

* Python 3.11 or later
* Git
* GitHub CLI (optional, for GitHub Releases)
* Windows, Linux or macOS

---

## Installation

Clone the repository:

```bash
git clone https://github.com/karthickkad/MAYDAY.git
```

Move into the project directory:

```bash
cd MAYDAY
```

Install dependencies:

```bash
pip install -r requirements.txt
```

(Optional) Verify GitHub CLI:

```bash
gh --version
```

(Optional) Authenticate GitHub CLI:

```bash
gh auth login
```

---

## Running MAYDAY

```bash
python main.py
```

---

## Creating a Release

MAYDAY includes an automated Release Manager.

Run:

```bash
python release.py
```

The Release Manager automatically:

* Generates the next project version
* Updates `config/version.json`
* Updates `README.md`
* Updates `CHANGELOG.md`
* Creates a Git commit
* Creates a Git tag
* Pushes commits and tags
* Optionally creates a GitHub Release

---

## Running the Test Suite

Run all unit tests:

```bash
python -m unittest discover -s tests -v
```

Generate a coverage report:

```bash
coverage run -m unittest discover
coverage report -m
coverage html
```

Current Layer 1 status:

* Automated unit tests
* High branch coverage target
* Modular test structure

---

## Project Structure

```text
MAYDAY/
│
├── config/
│   ├── settings.json
│   └── version.json
│
├── core/
│   ├── banner.py
│   ├── commands.py
│   ├── config.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── mayday.py
│   ├── utils.py
│   └── version.py
│
├── release/
│   ├── __init__.py
│   ├── version.py
│   ├── readme.py
│   ├── changelog.py
│   ├── git.py
│   ├── github.py
│   └── utils.py
│
├── tests/
│
├── logs/
│
├── main.py
├── release.py
├── README.md
├── CHANGELOG.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

---

## Project Modules

| Module                 | Description                     |
| ---------------------- | ------------------------------- |
| `main.py`              | Application entry point         |
| `core/mayday.py`       | Main application controller     |
| `core/commands.py`     | Command management framework    |
| `core/config.py`       | Configuration loader            |
| `core/logger.py`       | Logging framework               |
| `core/banner.py`       | Startup banner                  |
| `core/utils.py`        | Utility helper functions        |
| `core/version.py`      | Application version information |
| `core/exceptions.py`   | Custom exception classes        |
| `release.py`           | Release workflow controller     |
| `release/version.py`   | Version management              |
| `release/readme.py`    | README updater                  |
| `release/changelog.py` | CHANGELOG updater               |
| `release/git.py`       | Git automation                  |
| `release/github.py`    | GitHub Release automation       |
| `release/utils.py`     | Shared release utilities        |
| `tests/`               | Automated unit tests            |

---

## Layer 1 Architecture

```text
                     +----------------------+
                     |      main.py         |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |    MAYDAY Core       |
                     +----------+-----------+
                                |
        +-----------+-----------+-----------+-----------+
        |           |           |           |           |
        v           v           v           v           v
    Commands     Config      Logger      Utils      Banner
                                |
                                v
                          Log File Output

                     +----------------------+
                     |   Release Manager    |
                     +----------+-----------+
                                |
        +-----------+-----------+-----------+-----------+
        |           |           |           |           |
        v           v           v           v           v
    Version     README     CHANGELOG      Git      GitHub
```

The project follows a modular architecture where each component has a single responsibility. This improves maintainability, testability, scalability, and makes future feature development significantly easier.

---

## Layer 1 Completion

Layer 1 establishes the project's core infrastructure.

Completed:

* Modular project architecture
* Configuration management
* Command framework
* Logging framework
* Utility framework
* Custom exception handling
* Version management
* Release management
* README automation
* CHANGELOG automation
* Git integration
* GitHub Release integration
* Automated unit testing
* Structured project layout

---

## Roadmap

| Layer                             | Status     |
| --------------------------------- | -----------|
| Layer 1 – Project Foundation      | ✅ Complete|
| Layer 2 – Core Framework          | 🚧 Planned |
| Layer 3 – Device Management       | ⏳ Planned |
| Layer 4 – Communication Drivers   | ⏳ Planned |
| Layer 5 – Firmware Test Framework | ⏳ Planned |
| Layer 6 – Reporting Engine        | ⏳ Planned |
| Layer 7 – Plugin SDK              | ⏳ Planned |
| Layer 8 – AI-Assisted Analysis    | ⏳ Planned |

---

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Add or update tests.
4. Submit a pull request.

Please open an issue first if you plan to introduce major changes.

---

## Vision

MAYDAY aims to become a comprehensive open-source framework for AI, automation, and embedded systems development.

The long-term goal is to provide a professional platform for firmware validation, communication protocol testing, hardware automation, automated reporting, and extensible plugin development while maintaining a clean, modular, and well-tested architecture.

## Author

**Karthick B**

Embedded Systems • Firmware QA • Python Developer • Open-Source Enthusiast

* GitHub: https://github.com/karthickkad
* LinkedIn: https://www.linkedin.com/in/karthick-b-5294b0253

---

⭐ **If you find MAYDAY useful, consider giving it a star on GitHub!**

Contributions, feature requests, and feedback are always welcome.
