#!/usr/bin/env bash
set -e -o pipefail

cd /home/nonroot/.ssh/ || exit 1
ananta_args=()
ssh_command=()
hosts_csv="/home/nonroot/_autogen_hosts.csv"

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
        _HOSTS_CSV="$1"
        shift
        # Stop processing remaining arguments
        ssh_command=("$@")
        break
        ;;
    esac
done

if [[ -n "$_HOSTS_CSV" ]]; then
    # Modify the hosts.csv path to be under /home/nonroot/
    hosts_csv="/home/nonroot/$(basename "$_HOSTS_CSV")"
else
    echo "INFO: Will try to generate one using the SSH config..."
    /home/nonroot/sshconfig_to_ananta/main.py \
        --ssh /home/nonroot/.ssh/config \
        --relocate /home/nonroot/.ssh/ \
        "$hosts_csv"
fi

# Run the ananta command with the modified arguments
exec catatonit -- ananta "${ananta_args[@]}" "$hosts_csv" "${ssh_command[@]}"
