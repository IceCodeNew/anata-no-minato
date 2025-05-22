#!/usr/bin/env bash
set -e -o pipefail

# parse arguments
ananta_args=()
ssh_command=()
docker_run_args=('--interactive' '--tty')
while [[ $# -gt 0 ]]; do
    case "$1" in
    -[hH]|--help)
        # shellcheck disable=SC2016
        echo '
This helper script will automatically generate hosts file based on `~/.ssh/config`, issue the command as below:
(omit the hosts file argument)
`ananta -CS fastfetch`

In case you want to specify an existing hosts file,
   issue the command with the same arguments sequence as the original ananta command:
`ananta -t arch hosts.toml sudo pacman -Syu --noconfirm`
'
        exit 0
        ;;
    --helper-version)
        echo "anata-no-minato: REPLACE_ME_ANATA_NO_MINATO_VERSION"
        exit 0
        ;;
    --run-in-ci)
        docker_run_args=('--network' 'host')
        shift
        ;;
    -[nNsSeEcCvV]|--no-color|--separate-output|--allow-empty-line|--allow-cursor-control|--version)
        ananta_args+=("$1")
        shift
        ;;
    -[tTwWkK]|--host-tags|--terminal-width|--default-key)
        ananta_args+=("$1" "$2")
        shift 2
        ;;
    [!-]*.[cC][sS][vV]|[!-]*.[tT][oO][mM][lL])
        hosts_file="$1"
        shift
        ;;
    *)
        # Capture all remaining args (commands) in `ssh_command` and exit the parse loop
        ssh_command=("$@")
        break
        ;;
    esac
done

clean_out_date_ananta_images() {
    local latest_image_exist='false'
    local tags prune_list=()
    set +e
    IFS=$'\n' read -d "" -ra tags <<< "$(docker images --filter=reference='icecodexi/ananta' --format '{{.Tag}}')"
    set -e

    for tag in "${tags[@]}"; do
        if [[ "$tag" = 'REPLACE_ME_ANATA_NO_MINATO_VERSION' ]]; then
            latest_image_exist='true'
        else
            prune_list+=("icecodexi/ananta:$tag")
        fi
    done

    if [[ "$latest_image_exist" = 'false' ]]; then
        docker pull icecodexi/ananta:REPLACE_ME_ANATA_NO_MINATO_VERSION
    fi
    if [[ "${#prune_list[@]}" -gt '0' ]]; then
        docker rmi --force "${prune_list[@]}"
    fi
}

# main function

# Allow the nonroot user in the container to read files under ${HOME}/.ssh/ of other users
if [[ "$UID" -ne 65532 ]]; then
    docker_run_args+=('--user' 'root')
fi
if [[ -n "$hosts_file" ]]; then
    if [[ -f "$hosts_file" ]]; then
        docker_run_args+=('--volume' "${hosts_file}:/home/nonroot/$(basename "$hosts_file"):ro")
    else
        echo "ERROR: ${hosts_file} does not exist or is not a regular file."
        exit 1
    fi
fi

# preflight checklist
mkdir -p "${HOME}/.ssh/"
find "${HOME}/.ssh/" -type f -print0 | xargs -0 -r chmod 600
clean_out_date_ananta_images

docker run --rm \
    "${docker_run_args[@]}" \
    --volume /etc/localtime:/etc/localtime:ro \
    --volume "${HOME}/.ssh/:/home/nonroot/.ssh/:ro" \
    --cpu-shares 512 --memory 512M --memory-swap 512M \
    --security-opt no-new-privileges \
    icecodexi/ananta:REPLACE_ME_ANATA_NO_MINATO_VERSION \
        "${ananta_args[@]}" "$hosts_file" "${ssh_command[@]}"
