---
name: install-git-python
description: "Use this prompt to generate and validate OS-specific instructions for installing Git and Python (Windows/macOS/Linux)."
---

# Install Git and Python

## Intent
Create a one-shot, reproducible installation guide for Git and Python in a dev environment.

## Inputs
- `os` (required): one of `windows`, `macos`, `linux`
- `python_version` (optional): desired Python version (e.g., `3.12.2`, `3.11`)
- `git_version` (optional): desired Git version (or latest)
- `use_package_manager` (optional): `true`/`false`; if false provide direct installer links

## Output format
1. Check pre-requisites
2. Install Git
3. Install Python
4. Verify installations (`git --version`, `python --version`, `pip --version`)
5. Post-install notes (PATH, virtualenv, pipx, reboot)

## Example message
"Help me install Git and Python on Windows 11 with Python 3.12 and latest Git, including commands for PowerShell, validating paths, and optional chocolatey usage."

## Prompt
Generate an installation script + steps:
- Detect/assume OS from `os` input.
- Prefer package managers if `use_package_manager == true` (choco/homebrew/apt/dnf/pacman).
- Provide fallback direct download links.
- Include verification commands and common troubleshooting tips.
