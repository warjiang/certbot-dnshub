# Multi dns provider authentication plugin for certbot

[![Build Status](https://travis-ci.org/tengattack/certbot-dns-dnspod.svg?branch=master)](https://travis-ci.org/tengattack/certbot-dns-dnspod)
[![Coverage Status](https://coveralls.io/repos/github/tengattack/certbot-dns-dnspod/badge.svg?branch=master)](https://coveralls.io/github/tengattack/certbot-dns-dnspod?branch=master)
[![PyPI](https://img.shields.io/pypi/v/certbot-dns-dnspod.svg)](https://pypi.python.org/pypi/certbot-dns-dnspod)
[![PyPI](https://img.shields.io/pypi/pyversions/certbot-dns-dnspod.svg)](https://pypi.python.org/pypi/certbot-dns-dnspod)
[![PyPI](https://img.shields.io/pypi/l/certbot-dns-dnspod.svg)](https://pypi.python.org/pypi/certbot-dns-dnspod)


> English | [中文](README_zh-CN.md)

A certbot dns plugin to obtain certificates using dnspod.

## Obtain API Token
[https://www.dnspod.cn/console/user/security](https://www.dnspod.cn/console/user/security)

## Install

Pip:

```bash
sudo pip install git+https://github.com/tengattack/certbot-dns-dnspod.git
```

Snap:

```bash
sudo snap install certbot-dns-dnspod
sudo snap set certbot trust-plugin-with-root=ok
sudo snap connect certbot:plugin certbot-dns-dnspod
```

## Credentials File

```ini
dns_dnspod_api_id = 12345
dns_dnspod_api_token = 1234567890abcdef1234567890abcdef
```

```bash
chmod 600 /path/to/credentials.ini
```


## Obtain Certificates

```bash
certbot certonly -a dns-dnspod \
    --dns-dnspod-credentials /path/to/credentials.ini \
    -d example.com \
    -d "*.example.com"
```