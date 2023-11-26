# certbot-dnshub

> [English](README.md) | 中文


[![CI](https://github.com/warjiang/certbot-dnshub/workflows/CI/badge.svg?branch=main&event=push)](https://github.com/warjiang/certbot-dnshub/actions?query=event%3Apush+branch%3Amaster+workflow%3ACI+)
[![PyPI](https://img.shields.io/pypi/v/certbot-dnshub.svg)](https://pypi.org/project/certbot-dnshub/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/certbot-dnshub.svg)](https://pypi.org/project/certbot-dnshub/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/certbot-dnshub.svg)](https://pypi.org/project/certbot-dnshub/)
[![PyPI - License](https://img.shields.io/pypi/l/certbot-dnshub.svg)](https://pypi.org/project/certbot-dnshub/)

certbot-dnshub 是一个支持各种第三方 DNS 服务商的 Certbot DNS 插件，可以帮助你自动申请和更新 Let's Encrypt 通配符证书。

## 前置条件
1. 你已经有了一个域名，例如 `example.com`。
2. 对应的域名服务提供商已经提供了openapi或者sdk，例如dnspod、阿里云、腾讯云等。
3. 拿到openai或者sdk调用的配置信息


## 使用方式
以[dnspod](./assets/dnspod.md)使用为例，首先需要拿到dnspod的openapi的配置信息，然后执行如下命令：

1. 通过 docker 容器使用
    ```bash
    docker pull certbot/certbot
    docker run -it --rm --name certbot \
        -v "/etc/letsencrypt:/etc/letsencrypt" \
        -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
        -v "/path/to/credentials.ini:/path/to/credentials.ini" \
        --entrypoint /bin/sh certbot/certbot
    pip install certbot-dnshub 
    chmod 600 /path/to/credentials.ini
    certbot certonly -a dnshub \
            --dnshub-credentials /path/to/credentials.ini \
            -d www.example.com 
    ```
2. 通过 pip 安装使用
   ```bash
   python3 -m venv certbot
   source certbot/bin/activate
   pip install certbot certbot-dnshub
   chmod 600 /path/to/credentials.ini
   certbot certonly -a dnshub \
              --dnshub-credentials /path/to/credentials.ini \
              -d www.example.com 
   ```