# MAYDAY Release Process

## Purpose

This document describes the standard release workflow for the MAYDAY project.

The goal is to ensure that every release is:

- Tested
- Versioned
- Documented
- Tagged
- Reproducible

---

## Branch Strategy

main
: Stable production releases.

development
: Active development.

feature/*
: Individual feature development.

hotfix/*
: Critical production fixes.

---

## Development Workflow

1. Create a feature branch.

2. Implement the feature.

3. Add or update unit tests.

4. Ensure all tests pass.

5. Commit changes.

6. Merge into `development`.

---

## Before Every Release

## Code Quality

- All tests pass.
- No failing CI checks.
- No merge conflicts.
- Documentation updated.

---

## Documentation

Update if required:

- README.md
- CHANGELOG.md
- docs/project_status.md
- docs/development_log.md

---

## Version Update

Update:

config/version.json

or

config/version.py

Example:

Current

1.2.0

Next

1.3.0

---

## Release Steps

1

Verify repository status

```bash
git status
```

2

Run the complete test suite

```bash
python -m pytest
```

3

Commit changes

```bash
git add .

git commit -m "release: prepare v1.3.0"
```

4

Merge development into main

```bash
git checkout main

git merge development
```

5

Create release tag

```bash
git tag -a v1.3.0 -m "Release v1.3.0"
```

6

Push everything

```bash
git push origin main

git push origin development

git push origin --tags
```

---

## Release Checklist

- [ ] Version updated
- [ ] Tests passing
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Release committed
- [ ] Git tag created
- [ ] Tag pushed
- [ ] GitHub Release created

---

## Semantic Versioning

MAJOR.MINOR.PATCH

Examples

1.0.0

Major release

1.1.0

New features

1.1.1

Bug fixes

---

## Commit Message Convention

Feature

feat:

Bug Fix

fix:

Documentation

docs:

Refactor

refactor:

Tests

test:

Release

release:

Example

feat(provider): add provider health model

fix(factory): resolve provider lookup

docs: update architecture

test(provider): add health tests

release: prepare v1.3.0

---

## Rollback

Rollback to previous release

```bash
git checkout <tag>
```

Rollback latest commit

```bash
git revert HEAD
```

Rollback latest release

```bash
git checkout v1.2.0
```

---

## Future Improvements

- Automated version bumping
- Automatic CHANGELOG generation
- GitHub Release automation
- CI/CD deployment
- Release artifact generation
- Signed Git tags
