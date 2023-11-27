from lexicon.client import Client, _ClientOperations
from lexicon.config import ConfigResolver


def main():
    config = ConfigResolver().with_dict({
        'domain': "",
        'ttl': 600,
        'provider_name': "aliyun",
        'aliyun': {
            'auth_key_id': '',
            'auth_secret': '',
        },
    })
    client = Client(config)
    provider = client.provider_class(client.config)
    provider.authenticate()
    op = _ClientOperations(provider)
    for r in op.list_records():
        print(r)


if __name__ == "__main__":
    main()
