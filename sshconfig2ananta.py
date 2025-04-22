from typing import List
import argparse
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert SSH config to Ananta hosts csv.")
    parser.add_argument("--ssh", help="SSH config file.", default=Path.home() / ".ssh" / "config")
    parser.add_argument("--user", help="default ssh user", default="")
    parser.add_argument("csvfile", help="Path to the Ananta hosts csv.")
    return parser.parse_args()

def read_ssh_config(ssh_path):
    with open(ssh_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

class ConfigLine:
    """
        #alias,ip,port,username,key_path,tags(optional - colon separated)
        host-1,10.0.0.1,22,user,/home/user/.ssh/id_ed25519
        host-2,10.0.0.2,22,user,#,web
        host-3,10.0.0.3,22,user,#,arch:web
        host-4,10.0.0.4,22,user,#,ubuntu:db
    """
    alias: str
    ip: str
    port: str
    username: str
    key_path: str
    tags: str
    def __init__(self, alias: str, ip: str, port: str, username: str, key_path: str, tags: str = ""):
        self.alias = alias
        self.ip = ip
        self.port = port
        self.username = username
        self.key_path = key_path
        self.tags = tags
    
    def is_valid(self) -> bool:
        return all([self.alias, self.ip, self.port, self.username])

    def is_disabled(self) -> bool:
        tags = self.tags.split(":")
        for tag in tags:
            if tag.startswith("!ananta"):
                return True

        return False

    def to_string_with_feilds(self) -> str:
        return f"alias:{self.alias}\tip:{self.ip}\t\tport:{self.port}\tusername:{self.username}\tkey_path:{self.key_path}\ttags:{self.tags}"

    def to_string(self) -> str:
        if self.tags:
            return f"{self.alias},{self.ip},{self.port},{self.username},{self.key_path},{self.tags}"
        else:
            return f"{self.alias},{self.ip},{self.port},{self.username},{self.key_path}"

def strip_comment(line: str) -> str:
    """
    Remove comments from a line
    """
    line = line.replace("#tags", "ananta-tags")
    if "#" in line:
        return line[:line.index("#")].strip()
    return line.strip()

def convert_to_ananta(ssh_lines: List[str]) -> List[ConfigLine]:
    ananta_configs = []

    alias = ip = port = username = key_path = tags = ""

    at_host = False
    while ssh_lines:
        line = ssh_lines.pop(0)
        
        line = strip_comment(line)
        lower_line = line.lower()

        if lower_line.startswith("host "):
            if at_host:
                if not port:
                    # use default port if not provided
                    port = "22"

                if not key_path:
                    # use default key_path if not provided
                    key_path = "#"

                # host End, save the previous config
                ananta_configs.append(ConfigLine(alias, ip, port, username, key_path, tags))

            # reset values for the new host
            alias = ip = port = username = key_path = tags = ""
            
            at_host = True

            alias = line[len("host "):].strip() # host xxxx        
        elif lower_line.startswith("hostname "):
            ip = line[len("hostname "):].strip()
        elif lower_line.startswith("port "):
            port = line[len("port "):].strip()
            if not port.isdigit():
                print(f"Invalid port number: {port}")
                port = ""
            else:
                port = str(int(port))
        elif lower_line.startswith("user "):
            username = line[len("user "):].strip()
        elif lower_line.startswith("identityfile "):
            key_path = line[len("identityfile "):].strip()
        elif lower_line.startswith("ananta-tags "):
            tags = line[len("ananta-tags "):].strip().replace(",", ":")


    if at_host:
        ananta_configs.append(ConfigLine(alias, ip, port, username, key_path, tags))

    return ananta_configs

if __name__ == "__main__":
    args = parse_arguments()
    ssh_path = args.ssh
    csvfile = args.csvfile
    default_user = args.user

    ssh_lines = read_ssh_config(ssh_path)
    ananta_configs = convert_to_ananta(ssh_lines)

    with open(csvfile, 'w', encoding='utf-8') as file:
        for config in ananta_configs:
            if not config.is_valid():
                print(f"skipping invalid config:\t{config.to_string_with_feilds()}")
                continue
            if config.is_disabled():
                print(f"skipping disabled config:\t{config.to_string_with_feilds()}")
                continue

            if default_user:
                config.username = config.username if config.username else default_user

            file.write(config.to_string() + "\n")
