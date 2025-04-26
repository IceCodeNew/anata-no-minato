# Anata No Minato（あなたのみなと）

[English](README.md) | [中文](README_zh-Hans.md) | [日本語](README_ja.md)  
  
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/IceCodeNew/anata-no-minato?utm_source=oss&utm_medium=github&utm_campaign=IceCodeNew%2Fanata-no-minato&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
[![CodeQL](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/github-code-scanning/codeql)
  
这个项目将 [Ananta](https://github.com/cwt/ananta) 及其所需的完整运行时打包到一个极简的、安全加固过的容器镜像中，并带上了一些自动化脚本来简化使用体验。  
在使用该项目时，推荐将 `${HOME}/.ssh/` 挂载到容器中，容器会自动根据 `~/.ssh/config` 生成 `hosts.csv` 文件。  
  
由于经常需要在没有外网的环境中工作，我创建了这个项目用来方便在气隙环境中安装和使用 Ananta。  

## 项目如何得名

我电脑上的本地磁盘已经有太多 docker-XXX 命名的 git 仓库了，而我想每次都能少敲几个键就能跳转到这个项目下，所以这个项目不能叫 `docker-ananta`。  
而 `Ananta` 这个名字不是中文或日文讲话者习惯的发音，恰好省略掉一个 `n` 以后这个词就成了日语的 `Anata（あなた）`，这样我敲到第四个字母的时候就能跳转到这个项目了。  
而 `Minato（港）` 这个词在日语中可以表示“港口”的意思，可以从 docker 联想过来。两个词组合起来就得到了一首日本经典演歌的歌名。敬请欣赏：  
  
[![あなたのみなと～いい夫婦～ 松前ひろ子（2001）](https://i.ytimg.com/vi/sCRvjlTX8Fw/maxresdefault.jpg)](https://youtu.be/sCRvjlTX8Fw)

## 如何开始

以下命令会拉取一个极小的安装镜像，用于在当前系统上安装 `ananta` 的帮助脚本：

```shell
docker pull icecodexi/ananta:installer
docker run --rm --interactive --tty \
    --volume "$(pwd):/tmp/" \
    --security-opt no-new-privileges \
    icecodexi/ananta:installer \
        cp -f /usr/local/bin/ananta /tmp/ananta

sudo install -pvD ./ananta /usr/local/bin/
rm ./ananta
```

这个帮助脚本会自动根据 `~/.ssh/config` 生成 `hosts.csv` 文件，这样您执行 ananta 命令时就无需再指定 hosts.csv 文件：  
（注意这里相比上游的 ananta README，省略了中间的 hosts.csv 参数）  

```shell
ananta -CS fastfetch
```

如果您不需要上述功能，可使用和上游一致的参数顺序来指定 hosts.csv 文件，如下所示：  

```shell
ananta -t arch hosts.csv sudo pacman -Syu --noconfirm
```
