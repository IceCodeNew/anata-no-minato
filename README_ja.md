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
  
このプロジェクトは、[Ananta](https://github.com/cwt/ananta) とその完全なランタイム環境を内包した状態で、最小限のコンテナイメージを作成したものです。セキュリティを強化しつつ、不便さを感じさせないよう自動化スクリプトを導入し、操作性を向上させました。  
利用時には `${HOME}/.ssh/` ディレクトリをコンテナ内にマウントすることを推奨します。コンテナは `~/.ssh/config` に基づいて `hosts.toml` を自動生成します。  
  
接続が制限された環境での作業を想定し、エアギャップ環境におけるツールのインストールおよび運用を容易にするために、本プロジェクトを立ち上げました。  

## 使い始め方

以下の手順に従って、ananta のヘルパースクリプトをインストールしてください。  

```shell
curl -sSLROJ --fail -- \
    "https://github.com/IceCodeNew/anata-no-minato/releases/latest/download/ananta"

# スクリプトを実行する前に、内容を確認することを推奨します。
cat ./ananta

sudo install -pvD ./ananta /usr/local/bin/
rm ./ananta
```

このヘルパースクリプトは、`~/.ssh/config` をもとに `hosts.toml` ファイルを自動生成します。  
これにより、ananta ツールを実行する際に、あらかじめ `hosts.toml` を用意する必要がなくなります。  
実行例：  

```shell
ananta -CS fastfetch
```

なお、`hosts.toml` ファイルを指定したい場合は、公式 ananta ツールと同様のパラメータ順でコマンドを実行してください。  
実行例：  

```shell
ananta -t arch hosts.toml sudo pacman -Syu --noconfirm
```

## Ananta 用の SSH config 活用術

### タグの指定方法

SSH config 内で `#tags` 行を追加し、各ホストにタグを付与します。複数のタグはカンマ（`,`）またはコロン（`:`）で区切って記述できます。例：  

```sshconfig
Host mynas
    Hostname 1.1.1.1
    User root
    #tags tailscale,debian:nas,home
```

### 特定のホストを一時的に除外する方法

SSH コマンドを並行実行する際に特定のホストを一時的に除外したい場合は、対象ホストのタグリストに `!ananta` タグを追加してください。  

```sshconfig
Host do_not_ananta_in_this_host
    #tags home,debian,!ananta
```

### タグ行の一時無効化

`#tags` 行の先頭にもう一つの `#` を付けると、その行のタグが全て無効化されます。  
これにより、Ananta 実行時に該当ホストが通常通り接続対象となります。

```sshconfig
Host will_ananta_in_this_host
    ##tags home,debian,!ananta
```

## なぜ「あなたのみなと」と名付けたのか

私のパソコにはすでに「docker-XXX」という名前の Git リポジトリが多数存在しており、本プロジェクトはできるだけ少ないキー入力で移動できるように「docker-ananta」という名前を避けています。  
「Ananta」は、中国語や日本語話者にとってあまり馴染みのない発音ですが、「n」を一文字省略すると、日本語の「Anata（あなた）」に似た読みになることに気付きました。これにより、4 文字目まで入力すれば本プロジェクトに移動できるようになります。  
「Minato（港）」という言葉は、コンテナ（Docker）が港に停泊する船のように見えることから着想を得たものです。これら二つの言葉を組み合わせた結果、日本で広く知られる某有名演歌のタイトルになりました。ぜひご堪能ください：  
  
[![あなたのみなと～いい夫婦～ 松前ひろ子（2001）](https://i.ytimg.com/vi/sCRvjlTX8Fw/maxresdefault.jpg)](https://youtu.be/sCRvjlTX8Fw)
