# Anata No Minato（あなたのみなと）

[English](README.md) | [简体中文](README_zh-Hans.md) | [日本語](README_ja.md)  
  
[![CI](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/ananta.yml/badge.svg)](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/ananta.yml)
[![Unittest](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/unittest.yml/badge.svg)](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/unittest.yml)
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/IceCodeNew/anata-no-minato?utm_source=oss&utm_medium=github&utm_campaign=IceCodeNew%2Fanata-no-minato&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
![PyPI - Version](https://img.shields.io/pypi/v/sshconfig-to-ananta)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sshconfig-to-ananta)
[![CodeQL](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/IceCodeNew/anata-no-minato/actions/workflows/github-code-scanning/codeql)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/{owner}/{repo}/badge)](https://scorecard.dev/viewer/?uri=github.com/{owner}/{repo})
  
这个项目将 [Ananta](https://github.com/cwt/ananta) 及其所需的完整运行时打包到一个极简的、安全加固过的容器镜像中，并带上了一些自动化脚本来简化使用体验。  
在使用该项目时，推荐将 `${HOME}/.ssh/` 挂载到容器中，容器会自动根据 `~/.ssh/config` 生成 `hosts.csv` 文件。  
  
由于经常需要在没有外网的环境中工作，我创建了这个项目用来方便在气隙环境中安装和使用 Ananta。  

## 如何开始

在当前系统上安装 `ananta` 的帮助脚本：

```shell
curl -sSLROJ --fail -- \
    "https://github.com/IceCodeNew/anata-no-minato/releases/latest/download/ananta"

# 建议在执行任何脚本之前，都先检查脚本的内容
cat ./ananta

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

## 关于 SSH 配置文件的高级玩法

### 指定标签

你可以在 SSH 配置文件中通过添加 `#tags` 行来为机器分配标签。多个标签可用逗号（`,`）或冒号（`:`）分隔，示例如下：  

```sshconfig
Host mynas
    Hostname 1.1.1.1
    User root
    #tags tailscale,debian:nas,home
```

### 在生成 hosts.csv 时临时排除某些机器

如果你想在批量执行 SSH 命令时临时排除某些机器，只需在这些机器的标签列表中添加 `!ananta` 标签。  

```sshconfig
Host do_not_ananta_in_this_host
    #tags home,debian,!ananta
```

### 临时禁用所有标签

如果你想临时禁用某一行 `#tags`，只需在该行行首再加一个 `#`。这样可以在批量执行 SSH 命令时允许 Ananta 连接到这台机器。  

```sshconfig
Host will_ananta_in_this_host
    ##tags home,debian,!ananta
```

## 项目如何得名

我电脑上的本地磁盘已经有太多 docker-XXX 命名的 git 仓库了，而我想每次都能少敲几个键就能跳转到这个项目下，所以这个项目不能叫 `docker-ananta`。  
而 `Ananta` 这个名字不是中文或日文讲话者习惯的发音，恰好省略掉一个 `n` 以后这个词就成了日语的 `Anata（あなた）`，这样我敲到第四个字母的时候就能跳转到这个项目了。  
而 `Minato（港）` 这个词在日语中可以表示“港口”的意思，可以从 docker 联想过来。两个词组合起来就得到了一首日本经典演歌的歌名。敬请欣赏：  
  
[![あなたのみなと～いい夫婦～ 松前ひろ子（2001）](https://i.ytimg.com/vi/sCRvjlTX8Fw/maxresdefault.jpg)](https://youtu.be/sCRvjlTX8Fw)
