#!/usr/bin/env python3
# pyright: strict

import argparse
import logging
from pathlib import Path

from ssh_config_converter import convert_to_ananta_hosts


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert SSH config to Ananta hosts csv."
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
        "csvfile",
        help="Path the Ananta hosts file would be written to. (better set to a path that can safely overwrite)",
        type=Path,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    ssh_path = Path(args.ssh)
    csvfile = Path(args.csvfile)
    relocate = Path(args.relocate).resolve(strict=True) if args.relocate else None

    if csvfile.is_dir() or csvfile.is_symlink():
        raise IsADirectoryError(
            f"ERROR: {csvfile} is a directory OR a symlink. Script aborted to prevent data loss."
        )
    # ssh_path will be valided in convert_to_ananta_hosts()
    try:
        ananta_hosts = convert_to_ananta_hosts(ssh_path, relocate)
    except Exception as e:
        logging.error(f"Failed to convert SSH config to Ananta hosts: {e}")
        exit(1)

    try:
        with open(csvfile, "w", encoding="utf-8") as file:
            file.writelines([host.to_string() for host in ananta_hosts])
        logging.info(f"Successfully wrote Ananta hosts to {csvfile}.")
    except Exception as e:
        logging.error(f"Failed to write to {csvfile}: {e}")
        raise
