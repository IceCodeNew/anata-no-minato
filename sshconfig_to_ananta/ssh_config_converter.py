#!/usr/bin/env python3
# pyright: strict

import logging
import re
from pathlib import Path
from typing import Iterator, List, Optional, Tuple

from ananta_host import AnantaHost


def _read_ssh_config(ssh_path: Path) -> Iterator[str]:
    try:
        with open(ssh_path, "r", encoding="utf-8") as file:
            for line in file:
                yield line
    except FileNotFoundError:
        logging.warning(
            f"SSH config file could not be found in: {ssh_path}, hosts.csv could not be generated. "
            "To proceed, make sure you have provided a valid hosts.csv file. "
        )
    except Exception as e:
        logging.error(f"Failed to read SSH config file at {ssh_path}: {e}")


def _parse_valid_line(line: str) -> Optional[Tuple[str, str]]:
    ananta_tags_pattern = re.compile(r"^\s+#tags\s+", re.IGNORECASE)
    skip_pattern = re.compile(r"^\s*[#$]")
    line = ananta_tags_pattern.sub("ananta-tags ", line)
    if skip_pattern.match(line):
        return None

    try:
        key, value = line.strip().split(maxsplit=1)
        return key.lower(), value
    finally:
        return None


def _valid_host(alias: str) -> bool:
    """Hostname is not empty, and does not contain a wildcard"""
    return "*" not in alias and bool(alias.strip())


def _host_disabled(tags: List[str]) -> bool:
    return any(tag.startswith("!ananta") for tag in tags)


def _process_proxy_warning(alias: str) -> str:
    logging.warning(
        f"SSH host {alias} is configured with ProxyCommand/ProxyJump. "
        "Ananta does not support these configurations currently, which may prevent you from connecting to this host. "
    )
    return f"{alias}-needs-proxy"


def convert_to_ananta_hosts(
    ssh_path: Path, relocate: Optional[Path]
) -> List[AnantaHost]:
    ananta_hosts: List[AnantaHost] = []
    ssh_lines = _read_ssh_config(ssh_path)

    found_header_host = False
    alias = ip = port = username = key_path = ""
    tags = []
    for line in ssh_lines:
        parsed_line = _parse_valid_line(line)
        if not parsed_line:
            continue

        _key, _value = parsed_line
        if found_header_host:
            match _key:
                case "host":
                    # End of the previous host.
                    ananta_hosts.append(
                        AnantaHost(alias, ip, port, username, key_path, tags, relocate)
                    )
                    if not _valid_host(_value):
                        found_header_host = False
                        continue
                    # New host
                    alias = _value
                    ip = port = username = key_path = ""
                    tags = []
                case "hostname":
                    ip = _value
                case "port":
                    port = _value
                case "user":
                    username = _value
                case "identityfile":
                    key_path = _value
                case "ananta-tags":
                    tags: List[str] = re.split(r"[,:]+", _value)
                    if _host_disabled(tags):
                        found_header_host = False
                        continue
                case "proxycommand" | "proxyjump":
                    alias = _process_proxy_warning(alias)
                case _:
                    pass

        match _key:
            # TODO: support included configurations
            # case "include":
            case "host":
                if not _valid_host(_value):
                    continue
                # New host
                alias = _value
                ip = port = username = key_path = ""
                tags = []
                found_header_host = True
            case _:
                pass

    if _valid_host(alias):
        ananta_hosts.append(
            AnantaHost(alias, ip, port, username, key_path, tags, relocate)
        )
    return ananta_hosts
