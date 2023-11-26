from setuptools import setup
from setuptools import find_packages

version = '0.1.0'

install_requires = [
    'acme>=0.21.1',
    'certbot>=0.21.1',
    'dns-lexicon',
    'mock',
    'setuptools',
    'zope.interface',
]

# Read the long description from the README
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='certbot-dnshub',
    version=version,
    description="Multi dns provider authentication plugin for certbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/warjiang/certbot-dnshub',
    author="warjiang",
    author_email='1096409085@qq.com',
    license='Apache License 2.0',
    python_requires='>=3.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    package=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dnshub = certbot_dnshub.dnshub:Authenticator',
        ],
    },
)
