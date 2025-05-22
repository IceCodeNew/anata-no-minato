# Anata No Minato（あなたのみなと）

[English](README.md) | [简体中文](README_zh-Hans.md) | [日本語](README_ja.md)  
  
[![CI](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/ananta.yml/badge.svg)](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/ananta.yml)
[![Unittest](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/unittest.yml/badge.svg)](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/unittest.yml)
[![codecov](https://codecov.io/gh/IceCodeNew/anata-no-minato/graph/badge.svg?token=41TXXKSXUM)](https://codecov.io/gh/IceCodeNew/anata-no-minato)
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/IceCodeNew/anata-no-minato?utm_source=oss&utm_medium=github&utm_campaign=IceCodeNew%2Fanata-no-minato&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
![PyPI - Version](https://img.shields.io/pypi/v/sshconfig-to-ananta)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FIceCodeNew%2Fanata-no-minato%2Frefs%2Fheads%2Fmaster%2Fpyproject.toml)
[![CodeQL](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/github-code-scanning/codeql)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/IceCodeNew/anata-no-minato/badge)](https://scorecard.dev/viewer/?uri=github.com/IceCodeNew/anata-no-minato)
  
This project is an attempt to packaging the [Ananta](https://github.com/cwt/ananta) with its runtime into a minimum, hardened docker image, while also providing a convenient way to use it.  
It is recommended to bind mount the `${HOME}/.ssh/` into the container, and the container will automatically generate `hosts.toml` based on `~/.ssh/config` for you.  
  
Since it is routine for me to spend lot of my labour hours in an air-gapped environment, a docker image seems to be the best way to package some of my favourite tools.  

## How to start

Install the `ananta` helper script:

```shell
curl -sSLROJ --fail -- \
    "https://github.com/IceCodeNew/anata-no-minato/releases/latest/download/ananta"

# it is always a good idea to check the content of a script before executing it
cat ./ananta

sudo install -pvD ./ananta /usr/local/bin/
rm ./ananta
```

This helper script will automatically generate hosts.toml based on `~/.ssh/config`, issue the command as below:  
(omit the hosts.toml argument)  

```shell
ananta -CS fastfetch
```

In case you want to specify an existing hosts.toml,  
   issue the command with the same arguments sequence as the original ananta command:  

```shell
ananta -t arch hosts.toml sudo pacman -Syu --noconfirm
```

## Hacking SSH Config for Ananta

### Specify Tags

You can assign tags to hosts by including a `#tags` line in your SSH config. Separate multiple tags using either commas (`,`) or colons (`:`), as shown below:  

```sshconfig
Host mynas
    Hostname 1.1.1.1
    User root
    #tags tailscale,debian:nas,home
```

### Excluding a Host from hosts.toml Generation

To exclude a host from the generated `hosts.toml` file, add the `!ananta` tag to its tags list. Any host marked with this tag will be skipped during the generation process.  

```sshconfig
Host do_not_ananta_in_this_host
    #tags home,debian,!ananta
```

### Disabling the tags option

To disable a `#tags` line, simply add an extra `#` at the beginning, effectively re-enabling the SSH host.  

```sshconfig
Host will_ananta_in_this_host
    ##tags home,debian,!ananta
```

## Why named "Anata No Minato"

My local disk already has too many git repositories named `docker-XXX`. Since I want to save a few keystrokes when jumping into this project directory, I won't name it `docker-ananta`.
`Ananta` doesn't align with Chinese or Japanese pronunciation conventions. By omitting one 'n' it becomes the Japanese word `Anata` (あなた), which means "you" and gives me tab completion after typing just four letters.  
Meanwhile, `Minato` (みなと) in Japanese means "harbor" - a natural association with Docker containers. When combined, these form the title of a classic Japanese enka song. Please take a listen to it ;-)  
  
[![あなたのみなと～いい夫婦～ 松前ひろ子（2001）](https://i.ytimg.com/vi/sCRvjlTX8Fw/maxresdefault.jpg)](https://youtu.be/sCRvjlTX8Fw)
