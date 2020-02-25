#!/usr/bin/python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from manga_py.img2pdf.meta import __author__, __email__, __license__, __version__, __download_uri__

REQUIREMENTS = [
    'wheel',
    'Pillow',
    'packaging',
]

long_description = 'Please see %s' % (__download_uri__ or 'https://github.com/manga-py/manga-py')


release_status = 'Development Status :: 5 - Production/Stable'
if ~__version__.find('beta'):
    release_status = 'Development Status :: 4 - Beta'
if ~__version__.find('alpha'):
    release_status = 'Development Status :: 3 - Alpha'


setup(
    name='manga_py.img2pdf',
    packages=find_packages(exclude=('tests', '.mypy_cache', 'build')),
    include_package_data=True,
    version=__version__,
    description='Universal assistant download manga.',
    long_description=long_description,
    author=__author__,
    author_email=__email__,
    url=__download_uri__,
    zip_safe=False,
    download_url='{}/archive/{}.tar.gz'.format(__download_uri__, __version__),
    keywords=['manga-downloader', 'manga', 'manga-py'],
    license=__license__,
    classifiers=[  # look here https://pypi.python.org/pypi?%3Aaction=list_classifiers
        release_status,
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Environment :: Console',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.6',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'manga-py.img2pdf = manga_py.img2pdf:main',
            'manga_py.img2pdf = manga_py.img2pdf:main',
        ]
    }
)
