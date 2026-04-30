# Changelog

All notable changes to RapidTest will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.1] - 2026-04-29

### Added
- API reference documentation in `docs/api/reference.md`
- Documentation improvements across modules (asgi_test, data, http_test, performance, status_code)

### Changed
- Update version to 0.9.1

## [0.9.0] - 2026-04-23

### Added
- CLI `run` command now supports `--dir`, `--pattern`, `--fail-fast`, and `--dry-run` options
- CLI `scan` command now supports `--output`, `--format` (text/json), and `--dry-run` options
- Improved error handling and output formatting for both `run` and `scan` commands

## [0.8.0] - 2026-04-15

### Added
-Add cli "scan" command

### Removed
- CLI `init` command (functionality replaced by enhanced `scan` command)

## [0.7.2] - 2026-04-14

### Refactor
- CLI `run` less text

## [0.7.1] - 2026-04-12

### Fixed
- CLI `run` command execution logic

## [0.7.0] - 2026-04-12

### Added
- CLI `run` command to execute test files directly from the command line

## [0.6.0] - 2026-04-09

### Added
- Complete documentation restructuring with tutorials and API reference
- New tutorial guides for HTTPTest, ASGITest, and Performance testing
- API reference documentation for all modules
- MIT License added

### Changed
- Updated documentation to reflect new module structure
- Renamed internal references from `Test` to `HTTPTest`
- Improved mkdocs navigation structure

### Removed
- Deprecated `examples/` folder from documentation

## [0.5.0] - 2026-03-01

### Added
- Performance testing module with concurrent user simulation
- Data generation module with Faker integration

### Changed
- Improved error handling in HTTP requests

## [0.4.0] - 2026-02-01

### Added
- ASGI direct testing support
- CLI initialization command (`rapidtest init`)
- StatusCode enum for HTTP status codes

### Changed
- Restructured package exports

## [0.3.0] - 2026-01-01

### Added
- Basic HTTP testing (GET, POST, PUT, PATCH, DELETE)
- Response validation (status code, JSON body, keys)

## [0.2.0] - 2025-12-01

### Added
- Initial project setup
- Basic HTTP client functionality

## [0.1.0] - 2025-11-01

### Added
- First release (alpha)