#!/usr/bin/env bash
set -e -o pipefail

cd /home/nonroot/.ssh/ || exit 1

args=()
while [[ $# -gt 0 ]]; do
    case "$1" in
    -[kK]|--default-key)
        _DEFAULT_KEY="$2"
        # Modify the key path to be under /home/nonroot/.ssh/
        key_file=$(basename "$_DEFAULT_KEY")
        # Add the modified parameter
        args+=("$1" "/home/nonroot/.ssh/$key_file")
        shift 2
        ;;
    # Keep other parameters unchanged
    -[nNsSeEcCvV]|--no-color|--separate-output|--allow-empty-line|--allow-cursor-control|--version)
        args+=("$1")
        shift
        ;;
    -[tTwW]|--host-tags|--terminal-width)
        args+=("$1" "$2")
        shift 2
        ;;
    [!-]*)
        _HOSTS_CSV="$1"
        # Modify the hosts.csv path to be under /home/nonroot/
        hosts_file=$(basename "$_HOSTS_CSV")
        # Add the modified parameter
        args+=("/home/nonroot/$hosts_file")
        shift
        # Stop processing remaining arguments
        args+=("$@")
        break
        ;;
    esac
done

# Run the ananta command with the modified arguments
exec catatonit -- ananta "${args[@]}"
