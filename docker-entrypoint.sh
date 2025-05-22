#!/usr/bin/env bash
set -e -o pipefail

cd /home/nonroot/.ssh/ || exit 1
ananta_args=()
ssh_command=()
hosts_file="/home/nonroot/_autogen_hosts.toml"

while [[ $# -gt 0 ]]; do
    case "$1" in
    -[kK]|--default-key)
        _DEFAULT_KEY="$2"
        # Modify the key path to be under /home/nonroot/.ssh/
        key_file=$(basename "$_DEFAULT_KEY")
        # Add the modified parameter
        ananta_args+=("$1" "/home/nonroot/.ssh/$key_file")
        shift 2
        ;;
    # Keep other parameters unchanged
    -[nNsSeEcCvV]|--no-color|--separate-output|--allow-empty-line|--allow-cursor-control|--version)
        ananta_args+=("$1")
        shift
        ;;
    -[tTwW]|--host-tags|--terminal-width)
        ananta_args+=("$1" "$2")
        shift 2
        ;;
    ''|[!-]*)
        _hosts_file="$1"
        shift
        # Stop processing remaining arguments
        ssh_command=("$@")
        break
        ;;
    *)
        echo "FATAL: $0 failed to parse the arguments. Not supposed to reach here."
        exit 1
        ;;
    esac
done

if [[ -n "$_hosts_file" ]]; then
    # Modify the hosts file path to be under /home/nonroot/
    hosts_file="/home/nonroot/$(basename "$_hosts_file")"
else
    echo "INFO: Will try to generate one using the SSH config..."
    sshconfig_to_ananta \
        --ssh /home/nonroot/.ssh/config \
        --relocate /home/nonroot/.ssh/ \
        "$hosts_file"
fi

# Run the ananta command with the modified arguments
exec catatonit -- ananta "${ananta_args[@]}" "$hosts_file" "${ssh_command[@]}"
