# Anata No Minato（あなたのみなと）

[English](README.md) | [中文](README_zh-Hans.md) | [日本語](README_ja.md)  
  
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/IceCodeNew/anata-no-minato?utm_source=oss&utm_medium=github&utm_campaign=IceCodeNew%2Fanata-no-minato&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
  
このプロジェクトは、[Ananta](https://github.com/cwt/ananta) とその完全なランタイム環境を内包した状態で、最小限のコンテナイメージを作成したものです。セキュリティを強化しつつ、不便さを感じさせないよう自動化スクリプトを導入し、操作性を向上させました。  
利用時には `${HOME}/.ssh/` ディレクトリをコンテナ内にマウントすることを推奨します。コンテナは `~/.ssh/config` に基づいて `hosts.csv` を自動生成します。  
  
接続が制限された環境での作業が求められる状況を想定し、エアギャップ環境におけるツールのインストールおよび運用を容易にするために、本プロジェクトを立ち上げました。  

## なぜ「あなたのみなと」と名付けたのか

私のパソコにはすでに「docker-XXX」という名前の Git リポジトリが多数存在しており、このプロジェクトは、できるだけ少ないキータイプ数で移動できるようにしたかったため、「docker-ananta」という名前は避けたいんです。  
「ananta」は、中国語や日本語話者にとってあまり馴染みのない発音ですが、「n」を一文字省略すると、日本語の「anata（あなた）」に似た読みになることに気付きました。これにより、4 文字目まで入力すればこのプロジェクトに移動できるようになります。  
「minato（港）」は、コンテナ（Docker）が港に停泊する船のように見えることから着想を得たものです。この二つの言葉を組み合わせた結果、日本で広く知られる某有名演歌のタイトルになりました。ぜひご堪能ください：  
  
[![あなたのみなと～いい夫婦～ 松前ひろ子（2001）](https://i.ytimg.com/vi/sCRvjlTX8Fw/maxresdefault.jpg)](https://youtu.be/sCRvjlTX8Fw)

## 使い始め方

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
