# Multi dns provider authentication plugin for certbot

[![CI](https://github.com/warjiang/certbot-dnshub/workflows/CI/badge.svg?branch=main&event=push)](https://github.com/warjiang/certbot-dnshub/actions?query=event%3Apush+branch%3Amain+workflow%3ACI+)
[![PyPI](https://img.shields.io/pypi/v/certbot-dnshub.svg)](https://pypi.org/project/certbot-dnshub/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/certbot-dnshub.svg)](https://pypi.org/project/certbot-dnshub/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/certbot-dnshub.svg)](https://pypi.org/project/certbot-dnshub/)
[![PyPI - License](https://img.shields.io/pypi/l/certbot-dnshub.svg)](https://pypi.org/project/certbot-dnshub/)


> English | [中文](README_zh-CN.md)

Multi dns provider authentication plugin for certbot. It can help you automatically apply and update Let's Encrypt wildcard certificates.


## Usage
you can use this plugin with docker or pip. We recommend using docker.
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

example of credentials file as below:
```ini
dnshub_provider=dnspod
dnshub_api_id = 12345
dnshub_api_token = 1234567890abcdef1234567890abcdef
```


# FAQ