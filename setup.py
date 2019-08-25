try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Flash Cards Application',
    'author': 'CarlRad',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['flashCards'],
    'scripts': [],
    'name': 'flashCards'
}

setup(**config)
