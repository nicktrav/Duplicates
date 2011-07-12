try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Nick Travers',
    'url': 'http://www.nicktravers.id.au/blog/',
    'download_url': 'http://www.nicktravers.id.au/blog/',
    'author_email': 'n[dot]e[dot]travers[at]gmail[dot]com',
    'version':, '0.1',
    'instal_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)
