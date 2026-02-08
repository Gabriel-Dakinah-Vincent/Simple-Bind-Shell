# Changelog

All notable changes to this project will be documented in this file.

## [0.1.2] - 2026-02-08

### Changed
- Optimized socket receive buffering to reduce allocations
- Reduced logger lookup overhead in hot paths

## [0.1.1] - 2026-02-08

### Added
- Expanded CLI options and validation
- Structured logging and timeouts
- More complete README (usage, advanced scenarios, best practices)
- CI stability improvements and tooling pins

### Changed
- Refined project structure and exports
- Improved test coverage and configuration

## [0.1.0] - 2024-01-01

### Added
- Initial release
- Multi-threaded client handling
- CLI interface with click
- Configurable host, port, and connection limits
- Comprehensive error handling
- Logging support
- Command timeout protection
- Client connection timeout
- Graceful shutdown
- Cross-platform support

### Security
- Added security warnings and documentation
