# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.11.1] - 2026-09-01
### Fixed
- `auto` backend now warns on stderr when it falls back to OSC 52, so the
  fallback is visible even when stdout is redirected and no longer claims
  success on terminals that do not support OSC 52.

## [1.11.0] - 2026-08-13
### Added
- Linux OSC 52 text clipboard backend (writes to `/dev/tty`, not stdout)
- `--backend auto|osc52|wayland|xclip|xsel` and `COPYBUFFER_BACKEND` (CLI wins)

### Fixed
- Linux clipboard copy no longer reports success when `xclip`/`xsel`/`wl-copy` fails
- `DISPLAY` is treated as a hint, not proof that X11 is usable
- Failed graphical backends fall back to OSC 52 in `auto` mode
- Clipboard backend failure now exits with a nonzero status
- Unreachable X11 (`DISPLAY=localhost:N`) is skipped after a short TCP probe instead of blocking in `xclip`
- `xclip`/`wl-copy` success no longer stalls ~2s waiting on daemonized helper pipes

### Changed
- Linux text copy uses explicit backends instead of `pyperclip.copy()` so subprocess failures propagate
- Missing `DISPLAY` or graphical clipboard tools is no longer a hard startup failure on Linux

## [1.10.0] - 2026-07-12
### Added
- Linux ownership and permission restoration in `-p`/`--append` heredoc paste scripts
- Write-permission preflight in paste scripts (abort before writing if destination is not writable)
- Grok Build / Skeleton Swarm agent scaffolding (`AGENTS.md`, `GROK.md`, `.grok/`, `.crules/`)

### Changed
- `project_spec.md` refreshed to match current CLI surface and packaging

## [1.9.1] - 2025-01-05
### Fixed
- Fixed `UnicodeDecodeError` when processing files or stdin with non-UTF-8 encodings (e.g., UTF-16 with BOM)
- Added automatic encoding detection using chardet (if available) with fallback to common encodings
- Fixed undefined `is_gif` variable bug in `copy_image_to_clipboard()` function on Windows

### Changed
- All file and stdin reading operations now use encoding detection instead of assuming UTF-8
- Improved error handling for files with various text encodings

## [1.9.0] - 2025-01-XX
### Added
- Directory discovery with `.gitignore` support
- Recursive directory expansion with `-r/--recursive` flag
- File entry dataclass for better file handling


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