# How to start

```shell
docker pull icecodexi/ananta:latest
mkdir -p "${HOME}/.ssh/"
find "${HOME}/.ssh/" -type f -print0 | xargs -0 -r chmod 600

_extra_args=()
if [[ "$UID" -eq '0' ]]; then
    _extra_args+=('--user' 'root')
fi

# Will automatic generate hosts.csv based on ~/.ssh/config if it does not exist
_hosts_csv="$(pwd)/hosts.csv"
if [[ -f "${_hosts_csv}" ]]; then
    hosts_csv="${_hosts_csv}"
    _extra_args+=('--volume' "${_hosts_csv}:/home/nonroot/hosts.csv:ro")
fi

export _extra_args hosts_csv
# put this function definition in your ~/.bashrc
ananta() {
    docker run --rm --interactive --tty \
        "${_extra_args[@]}" \
        --volume /etc/localtime:/etc/localtime:ro \
        --volume "${HOME}/.ssh/:/home/nonroot/.ssh/:ro" \
        --cpu-shares 512 --memory 512M --memory-swap 512M \
        --security-opt no-new-privileges \
        icecodexi/ananta:latest "$hosts_csv" \
            "$@"
}

## Example for issuing command `whoami` to multiple hosts
ananta whoami
```
