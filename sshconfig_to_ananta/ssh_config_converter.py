#!/usr/bin/env python3
# pyright: strict

import re
from pathlib import Path
from typing import List

from ananta_host import AnantaHost


def _read_ssh_config(ssh_path: Path) -> List[str]:
    try:
        with open(ssh_path, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"""
WARN: SSH config file could not found in: {ssh_path}, hosts.csv could not be generated.
To proceed, make sure you have provided a valid hosts.csv file.
""")
        return []


def _pop_valid_line(ssh_lines: List[str]) -> str | None:
    ananta_tags_pattern = re.compile(r"^\s+#tags\s+", re.IGNORECASE)
    skip_pattern = re.compile(r"^\s*[#$]")
    if ssh_lines:
        line = ananta_tags_pattern.sub("ananta-tags ", ssh_lines.pop(0))
        if not skip_pattern.match(line):
            line = line.strip().lower()
            if line:
                return line


def _valid_host(alias: str) -> bool:
    """skip configuration applies to multiple hosts, e.g.

    Host *
        Include "/home/nonroot/.step/ssh/includes"
    """
    if "*" in alias:
        return False
    return bool(alias)


def _host_disabled(tags: List[str]) -> bool:
    """add a `!ananta` tag to disable a host. Disabled hosts will not be added to hosts.csv. e.g.

    Host mynas
        #tags home,debian,!ananta
    """
    for tag in tags:
        if tag.startswith("!ananta"):
            return True
    return False


def convert_to_ananta_hosts(ssh_path: Path, relocate: Path | None) -> List[AnantaHost]:
    ananta_hosts: List[AnantaHost] = []
    ssh_lines = _read_ssh_config(ssh_path)

    found_header_host = False
    alias = ip = port = username = key_path = ""
    tags = []
    while ssh_lines:
        line = _pop_valid_line(ssh_lines)
        if not line:
            continue

        _key, _value = line.split(maxsplit=1)
        if found_header_host:
            match _key:
                case "host":
                    # End of the previous host.
                    ananta_hosts.append(AnantaHost(alias, ip, port, username, key_path, tags, relocate))

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
                    alias = f"{alias}-needs-proxy"
                case _:
                    pass

        match _key:
            case "include":
                # TODO: support included configurations
                pass
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
        ananta_hosts.append(AnantaHost(alias, ip, port, username, key_path, tags, relocate))
    return ananta_hosts
