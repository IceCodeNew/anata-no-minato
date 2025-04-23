# Anata No Minato（あなたのみなと）

[English](README.md) | [中文](README_zh-Hans.md) | [日本語](README_ja.md)  
  
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/IceCodeNew/anata-no-minato?utm_source=oss&utm_medium=github&utm_campaign=IceCodeNew%2Fanata-no-minato&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
[![CodeQL](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/github-code-scanning/codeql)
  
This project is an attempt to packaging the [Ananta](https://github.com/cwt/ananta) with its runtime into a minimum, hardened docker image, while also providing a convenient way to use it.  
It is recommended to bind mount the `${HOME}/.ssh/` into the container, and the container will automatically generate `hosts.csv` based on `~/.ssh/config` for you.  
  
Since it is routine for me to spend lot of my labour hours in an air-gapped environment, a docker image seems to be the best way to package some of my favourite tools.  

## Why named "Anata No Minato"

My local disk already has too many git repositories named `docker-XXX`. Since I want to save a few keystrokes when jumping into this project directory, I won't name it `docker-ananta`.
`Ananta` doesn't align with Chinese or Japanese pronunciation conventions. By omitting one 'n' it becomes the Japanese word `Anata` (あなた), which means "you" and gives me tab completion after typing just four letters.  
Meanwhile, `Minato` (みなと) in Japanese means "harbor" - a natural association with Docker containers. When combined, these form the title of a classic Japanese enka song. Please take a listen to it ;-)  
  
[![あなたのみなと～いい夫婦～ 松前ひろ子（2001）](https://i.ytimg.com/vi/sCRvjlTX8Fw/maxresdefault.jpg)](https://youtu.be/sCRvjlTX8Fw)

## How to start

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
