# Anata No Minato（あなたのみなと）

This project is an attempt to packaging the [Ananta](https://github.com/cwt/ananta) with its runtime into a minimum, hardened docker image, while also providing a convenient way to use it.  
It is recommended to bind mount the `${HOME}/.ssh/` into the container, and the container will automatically generate `hosts.csv` based on `~/.ssh/config` for you.  
  
Since it is routine for me to spend lot of my labour hours in an air-gapped environment, a docker image seems to be the best way to package some of my favourite tools.  
  
这个项目将 [Ananta](https://github.com/cwt/ananta) 及其所需的完整运行时打包到一个极简的、安全加固过的容器镜像中，并带上了一些自动化脚本来简化使用体验。  
在使用该项目时，推荐将 `${HOME}/.ssh/` 挂载到容器中，容器会自动根据 `~/.ssh/config` 生成 `hosts.csv` 文件。  
  
由于经常需要在没有外网的环境中工作，我创建了这个项目用来方便在气隙环境中安装和使用 Ananta。  

## Why named "Anata No Minato"

My local disk already has too many git repositories named `docker-XXX`. Since I want to save a few keystrokes when jumping into this project directory, I won't name it `docker-ananta`.
`Ananta` doesn't align with Chinese or Japanese pronunciation conventions. By omitting one 'n' it becomes the Japanese word `Anata` (あなた), which means "you" and gives me tab completion after typing just four letters.  
Meanwhile, `Minato` (みなと) in Japanese means "harbor" - a natural association with Docker containers. When combined, these form the title of a classic Japanese enka song. Please take a listen to it ;-)  
  
我电脑上的本地磁盘已经有太多 docker-XXX 命名的 git 仓库了，而我想每次都能少敲几个键就能跳转到这个项目下，所以这个项目不能叫 `docker-ananta`。  
而 `ananta` 这个名字不是中文或日文讲话者习惯的发音，恰好省略掉一个 `n` 以后这个词就成了日语的 `anata`，这样我敲到第四个字母的时候就能跳转到这个项目了。  
而 `minato` 这个词在日语中可以表示“港口”的意思，可以从 docker 联想过来。这样一组合就得到了一首日本经典演歌的歌名。敬请欣赏：  
  
[![](https://i.ytimg.com/vi/sCRvjlTX8Fw/maxresdefault.jpg)](https://www.youtube.com/embed/sCRvjlTX8Fw)

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
