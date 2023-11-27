"""Multi dns provider authentication plugin for certbot."""
import logging

import zope.interface

from lexicon.client import Client, _ClientOperations
from lexicon.config import ConfigResolver

from certbot import interfaces
from certbot.plugins import dns_common
from certbot_dnshub.error import ErrUnsupportedDNSProvider, ErrInvalidDnsConfig

logger = logging.getLogger(__name__)

ACCOUNT_URL = 'https://www.dnspod.cn/console/user/security'


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """Multi dns provider authentication plugin for certbot

    This Authenticator uses lexicon to fulfill a dns-01 challenge.
    """

    description = 'Obtain certificates using a DNS TXT record.'
    ttl = 600

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None
        self.domain_operation = dict()
        self.key_prefix = 'dnshub_'
        self.preserved_keys = [self.key_prefix + k for k in ['provider']]

    @classmethod
    def add_parser_arguments(cls, add, default_propagation_seconds: int = 10):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds)
        add('credentials', help='DNSPod credentials INI file.')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using the lexicon library.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'DNSHub credentials INI file',
            {
                'provider': 'Name of the DNS provider to use',
                # 'api_id': 'API ID for DNSPod account, obtained from {0}'.format(ACCOUNT_URL),
                # 'api_token': 'API Token for DNSPod account, obtained from {0}'.format(ACCOUNT_URL)
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_operation(domain).create_record(rtype='TXT', name=validation_name, content=validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_operation(domain).delete_record(rtype='TXT', name=validation_name, content=validation)

    def _get_operation(self, domain):
        if domain in self.domain_operation:
            return self.domain_operation[domain]

        if not self._check_provider_config():
            raise ErrInvalidDnsConfig

        extra_cfg = {}
        for k in self.credentials.confobj:
            if k in self.preserved_keys:
                continue
            key_without_prefix = k[len(self.key_prefix):]
            extra_cfg[key_without_prefix] = self.credentials.confobj.get(k)

        config = ConfigResolver().with_dict({
            'domain': domain,
            'ttl': self.ttl,
            'provider_name': self.credentials.conf("provider"),
            self.credentials.conf("provider"): extra_cfg
        })
        client = Client(config)
        provider = client.provider_class(client.config)
        provider.authenticate()
        op = _ClientOperations(provider)
        self.domain_operation[domain] = op
        return op

    def _check_provider_config(self):
        # need to check config according to provider
        # e.g.
        # dnspod must input auth_username/auth_token
        # aliyundns must input auth_key_id/auth_secret
        provider_name = self.credentials.conf("provider")

        # only dns provider in whitelist is supported
        if provider_name not in ['dnspod', 'aliyun']:
            raise ErrUnsupportedDNSProvider
        # if provider_name == 'dnspod':
        #     pass
        # elif provider_name == 'aliyun':
        #     pass
        return True
