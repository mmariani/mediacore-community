try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys
from mediacore import __version__ as VERSION

install_requires = [
    'WebTest == 1.2',
    'Pylons == 0.10',
    'WebOb == 1.0.7',
    'WebHelpers == 1.0',
    'SQLAlchemy == 0.6.8',
    'sqlalchemy-migrate == 0.6',
    'Genshi == 0.6',
    'Babel == 0.9.6',
    'Routes == 1.12.3',
    'repoze.who == 1.0.18',
    'repoze.what-pylons == 1.0',
    'repoze.what-quickstart',
    'Paste == 1.7.4',
    'PasteDeploy == 1.3.3',
    'PasteScript == 1.7.3',
    'ToscaWidgets == 0.9.9',
    'tw.forms == 0.9.9',
    'MySQL-python >= 1.2.2',
    'BeautifulSoup == 3.0.7a',
        # We monkeypatch this version of BeautifulSoup in mediacore.__init__
        # Patch pending: https://bugs.launchpad.net/beautifulsoup/+bug/397997
    'PIL == 1.1.6',
        # The original PIL 1.1.6 package won't install via setuptools so this
        # this setup script installs http://dist.repoze.org/PIL-1.1.6.tar.gz
    'akismet == 0.2.0',
    'feedparser >= 4.1', # needed only for rss import script
    'gdata > 2, < 2.1',
    'unidecode',
    'decorator',
    'simplejson',
    'hachoir_metadata == 1.3.3',
    'hachoir_parser == 1.3.4',
]

if sys.version_info < (2, 7):
    # importlib is included in Python 2.7
    # however we can't do try/import/except because this might generate eggs
    # with missing requires which can not be used in other environments
    # see https://github.com/mediacore/mediacore-community/issues#issue/44
    install_requires.append('importlib')

if sys.version_info < (2, 5):
    # These package comes bundled in Python >= 2.5 as xml.etree.cElementTree.
    install_requires.append('elementtree >= 1.2.6, < 1.3')
    install_requires.append('cElementTree >= 1.0.5, < 1.1')

extra_arguments_for_setup = {}

# extractors are declared separately so it is easier for 3rd party users
# to use them for other packages as well...
extractors = [
    ('lib/unidecode/**', 'ignore', None),
    ('tests/**', 'ignore', None),
    ('**.py', 'python', None),
    ('templates/**.html', 'genshi', {
            'template_class': 'genshi.template.markup:MarkupTemplate'
        }),
    ('public/**', 'ignore', None),
]
extra_arguments_for_setup['message_extractors'] = {'mediacore': extractors}

setup(
    name='MediaCore',
    version=VERSION,
    description='A audio, video and podcast publication platform.',
    author='MediaCore Inc.',
    author_email='info@mediacore.com',
    url='http://mediacorecommunity.org/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Framework :: TurboGears :: Applications',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP :: Site Management'
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Multimedia :: Sound/Audio',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        ],

    install_requires=install_requires,
    paster_plugins=[
        'PasteScript',
        'Pylons',
    ],

    test_suite='nose.collector',
    tests_require=[
        'WebTest',
        ],

    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    package_data={'mediacore': ['i18n/*/LC_MESSAGES/*.mo']},
    zip_safe=False,

    entry_points="""
    [paste.app_factory]
    main = mediacore.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,

    **extra_arguments_for_setup
)
