# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.8.0] - 2025-08-20
### Added
- Wayland clipboard support via `wl-clipboard` with improved dependency checks
- Documentation updates for Wayland requirements

## [1.5.0] - 2024-03-20
### Added
- STDIN support for piping content directly to clipboard
- Directory mode for copying multiple files
- Verbose output option (-v, --verbose)
- Debug mode for troubleshooting
- Improved error handling and messages

### Changed
- Renamed --header to -i/--include-header for clarity
- Updated command-line interface for better usability
- Improved documentation and examples
- Streamlined dependency checking

### Fixed
- Image file handling in directory mode
- Error messages for missing dependencies
- Clipboard handling on different platforms

## [1.7.0] - 2025-08-13
### Added
- New `-p/--paste` flag to copy a shell heredoc script that recreates the given files on paste
- New `--append` flag to generate heredoc that appends to target files instead of overwriting
- Keeps existing `-a/--attachment` for Discord formatting (unchanged)

### Changed
- Bumped version to 1.7.0

### Notes
- Heredoc uses a random, content-safe delimiter and single-quoted terminator to avoid interpolation

## [1.0.4] - 2024-03-01
### Added
- Initial release
- Basic file to clipboard functionality
- Image file support
- Discord attachment formatting
- Header inclusion option
- Dependency checking 