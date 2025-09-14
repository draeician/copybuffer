# Wayland clipboard support

- **Role:** Coder

## Summary
CopyBuffer fails on CachyOS when running under Wayland because `pyperclip` cannot find a clipboard mechanism. Even with `xclip` and `xsel` installed, Wayland sessions require `wl-clipboard` (`wl-copy`/`wl-paste`).

## Deliverables
- Detect Wayland environments and attempt to use `wl-clipboard` when available.
- Provide a helpful error message suggesting installation of `wl-clipboard` if no copy/paste mechanism is found.
- Update documentation to mention `wl-clipboard` as a requirement for Wayland-based systems (e.g. CachyOS).

## Acceptance checks
- Running `cb` under Wayland with `wl-clipboard` installed successfully copies and pastes text.
- Running under Wayland without `wl-clipboard` shows a clear install hint instead of an unhandled error.
- `pytest` passes.
