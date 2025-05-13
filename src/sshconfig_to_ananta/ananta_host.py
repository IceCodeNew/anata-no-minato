#!/usr/bin/env python3
# pyright: strict

from pathlib import Path
from typing import List, Optional


class AnantaHost:
    """Represents an Ananta host entry.

    This class stores the configuration details for connecting to a host
    via SSH, intended for use with the Ananta system.

    The expected format for representing a host is a comma-separated string:
    alias,ip,port,username,key_path[,tags]

    Where:
        - alias: A short name or identifier for the host.
        - ip: The IP address or hostname of the host.
        - port: The SSH port number (defaults to 22 if empty or omitted).
        - username: The username for SSH login (defaults to 'root' if empty or omitted).
        - key_path: The path to the SSH private key file. Use '#' if not applicable or managed elsewhere.
        - tags (optional): Colon-separated tags for categorization (e.g., 'web', 'db', 'arch:web').

    Examples:
        - host-1,10.0.0.1,22,user,/home/user/.ssh/id_ed25519
        - host-2,10.0.0.2,22,user,#,web
        - host-3,10.0.0.3,22,user,#,arch:web
        - host-4,10.0.0.4,22,user,#,ubuntu:db
    """

    alias: str
    ip: str
    port: int
    username: str
    key_path: str
    tags: List[str]
    relocate: Optional[Path]

    def __init__(
        self,
        alias: str,
        ip: str,
        port: str,
        username: str,
        key_path: str,
        tags: List[str],
        relocate: Optional[Path],
    ):
        _err_msg = f"""
  alias: {alias}
  ip: {ip}
  port: {port}
  username: {username}
  key_path: {key_path}
  tags: {tags}
  relocate: {relocate}
"""

        if not alias:
            raise ValueError(f"ERROR: alias cannot be empty.{_err_msg}")
        self.alias = alias

        if not ip:
            raise ValueError(f"ERROR: ip cannot be empty.{_err_msg}")
        self.ip = ip

        try:
            self.port = int(port) if port else 22
            if not (0 < self.port < 65536):
                raise ValueError(
                    f"ERROR: Port number {port} must be greater than 0 and less than 65536.{_err_msg}"
                )
        except (ValueError, TypeError) as e:
            raise ValueError(f"ERROR: Invalid port number: {port}.{_err_msg}") from e

        self.username = username if username else "root"

        self.key_path = key_path if key_path else "#"
        if key_path and relocate:
            key_path_obj = relocate / Path(key_path).name
            if not key_path_obj.is_file():
                raise FileNotFoundError(
                    f"ERROR: SSH Key {key_path} could not be found OR it is not a regular file.{_err_msg}"
                )
            self.key_path = str(key_path_obj)

        self.tags = tags if tags else []

        self.relocate = relocate if isinstance(relocate, Path) else None

    def to_string_with_fields(self) -> str:
        return (
            f"  alias:    {self.alias}\n"
            f"  ip:       {self.ip}\n"
            f"  port:     {str(self.port)}\n"
            f"  username: {self.username}\n"
            f"  key_path: {self.key_path}\n"
            f"  tags:     {','.join(self.tags)}\n"
        )

    def to_string(self) -> str:
        parts = [self.alias, self.ip, str(self.port), self.username, self.key_path]
        if self.tags:
            parts.append(":".join(self.tags))
        return ",".join(parts) + "\n"
