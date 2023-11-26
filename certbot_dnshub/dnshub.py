"""Multi dns provider authentication plugin for certbot."""
import logging

import zope.interface

from lexicon.client import Client, _ClientOperations
from lexicon.config import ConfigResolver

from certbot import interfaces
from certbot.plugins import dns_common
from certbot_dnshub.error import ErrUnsupportedDNSProvider

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
                'api_id': 'API ID for DNSPod account, obtained from {0}'.format(ACCOUNT_URL),
                'api_token': 'API Token for DNSPod account, obtained from {0}'.format(ACCOUNT_URL)
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_operation(domain).create_record(rtype='TXT', name=validation_name, content=validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_operation(domain).delete_record(rtype='TXT', name=validation_name, content=validation)

    def _get_operation(self, domain):
        if domain in self.domain_operation:
            return self.domain_operation[domain]
        # only tested dnspod now
        if self.credentials.conf("provider") not in ['dnspod']:
            raise ErrUnsupportedDNSProvider

        """
        extra_cfg = {
            k: self.credentials.confobj.get(k)
            for k in self.credentials.confobj
            if k != "provider"
        }
        """

        config = ConfigResolver().with_dict({
            'domain': domain,
            'ttl': self.ttl,
            'provider_name': self.credentials.conf("provider"),
            self.credentials.conf("provider"): {
                'auth_username': self.credentials.conf('api_id'),
                'auth_token': self.credentials.conf('api_token'),
            }
        })
        client = Client(config)
        provider = client.provider_class(client.config)
        provider.authenticate()
        op = _ClientOperations(provider)
        self.domain_operation[domain] = op
        return op
