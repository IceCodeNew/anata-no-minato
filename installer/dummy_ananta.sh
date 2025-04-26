#!/usr/bin/env bash
set -e -o pipefail

get_latest_ananta_image() {
    local tags today prune_list pull
    pull='true'
    set +e
    IFS=$'\n' read -d "" -ra tags <<< "$(docker images --filter=reference='icecodexi/ananta' --format '{{.Tag}}')"
    set -e

    today=$(date +%Y-%m-%d)
    for tag in "${tags[@]}"; do
        case "$tag" in
            "$today") pull='false';;
            'latest') ;;
                   *) prune_list+=("icecodexi/ananta:$tag");;
        esac
    done

    if [[ "$pull" != 'false' ]]; then
        docker pull icecodexi/ananta:latest
        docker tag icecodexi/ananta:latest "icecodexi/ananta:${today}"
    fi
    if [[ "${#prune_list[@]}" -gt '0' ]]; then
        docker rmi --force "${prune_list[@]}"
    fi
}

# parse arguments
inputs=()
append=()
while [[ $# -gt 0 ]]; do
    case "$1" in
    -[hH]|--help)
        # shellcheck disable=SC2016
        echo '
This helper script will automatically generate hosts.csv based on `~/.ssh/config`, issue the command as below:
(omit the hosts.csv argument)
`ananta -CS fastfetch`

In case you want to specify an existing hosts.csv,
   issue the command with the same arguments sequence as the original ananta command:
`ananta -t arch hosts.csv sudo pacman -Syu --noconfirm`
'
        exit 0
        ;;
    -[nNsSeEcCvV]|--no-color|--separate-output|--allow-empty-line|--allow-cursor-control|--version)
        inputs+=("$1")
        shift
        ;;
    -[tTwWkK]|--host-tags|--terminal-width|--default-key)
        inputs+=("$1" "$2")
        shift 2
        ;;
    [!-]*)
        might_be_hosts_csv="$1"
        shift
        # Stop processing remaining arguments
        append=("$@")
        break
        ;;
    esac
done

# main function
docker_run_args=()

# Allow the nonroot user in the container to read files under ${HOME}/.ssh/ of other users
if [[ "$UID" -ne 65532 ]]; then
    docker_run_args+=('--user' 'root')
fi
if [[ -n "$might_be_hosts_csv" ]]; then
    absolute_hosts_csv="$(realpath "$might_be_hosts_csv")"
    if [[ -f "$absolute_hosts_csv" ]]; then
        docker_run_args+=('--volume' "${absolute_hosts_csv}:/home/nonroot/$(basename "$absolute_hosts_csv"):ro")
    else
        append=("$might_be_hosts_csv" "${append[@]}")
    fi
fi

# preflight checklist
mkdir -p "${HOME}/.ssh/"
find "${HOME}/.ssh/" -type f -print0 | xargs -0 -r chmod 600
get_latest_ananta_image

docker run --rm --interactive --tty \
    "${docker_run_args[@]}" \
    --volume /etc/localtime:/etc/localtime:ro \
    --volume "${HOME}/.ssh/:/home/nonroot/.ssh/:ro" \
    --cpu-shares 512 --memory 512M --memory-swap 512M \
    --security-opt no-new-privileges \
    icecodexi/ananta:latest "$absolute_hosts_csv" \
        "${inputs[@]}" "${append[@]}"
