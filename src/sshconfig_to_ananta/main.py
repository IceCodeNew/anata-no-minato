#!/usr/bin/env python3
# pyright: strict

import argparse
import logging
import sys
from pathlib import Path
from types import ModuleType
from typing import Optional

from sshconfig_to_ananta.ssh_config_converter import convert_to_ananta_hosts

tomli_w: Optional[ModuleType] = None
try:
    import tomli_w
except ImportError:
    pass  # toml support is optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert SSH config to a list of SSH servers that Ananta can recognize. "
        "Emits TOML output if the 'tomli_w' module is available."
    )
    parser.add_argument(
        "--ssh",
        help="SSH config file.",
        default=Path.home() / ".ssh" / "config",
        type=Path,
    )
    parser.add_argument(
        "--relocate",
        help="Relocate the SSH directory to the specified path. (for the container use cases)",
        default="",
        type=Path,
    )
    parser.add_argument(
        "server_list",
        help="Path the list of SSH servers would be written to. (better set to a path that can safely overwrite)",
        type=Path,
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    ssh_path = args.ssh
    server_list = Path(args.server_list)
    relocate = Path(args.relocate).resolve(strict=True) if args.relocate else None

    if tomli_w and server_list.suffix != ".toml":
        server_list = server_list.with_suffix(".toml")
    if server_list.is_dir() or server_list.is_symlink():
        raise IsADirectoryError(
            f"ERROR: {server_list} is a directory OR a symlink. Script aborted to prevent data loss."
        )
    if relocate and not relocate.is_dir():
        raise NotADirectoryError(f"ERROR: relocate path {relocate} is not a directory.")

    # ssh_path will be valided in convert_to_ananta_hosts()
    try:
        ananta_hosts = convert_to_ananta_hosts(ssh_path, relocate)
    except Exception as e:
        logging.error("Failed to convert SSH config to Ananta hosts: %s", e)
        sys.exit(1)

    try:
        with open(server_list, "w", encoding="utf-8") as file:
            if tomli_w:
                toml_data = {host.alias: host.dump_host_info() for host in ananta_hosts}
                file.write(tomli_w.dumps(toml_data))
            else:
                file.writelines(
                    host.dump_comma_separated_str() for host in ananta_hosts
                )
        logging.info("Successfully wrote Ananta hosts to %s.", server_list)
    except Exception as e:
        logging.exception("Failed to write to %s: %s", server_list, e)
        raise


if __name__ == "__main__":
    main()
