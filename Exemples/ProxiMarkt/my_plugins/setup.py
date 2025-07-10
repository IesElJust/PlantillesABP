from setuptools import setup

setup(
    name='mkdocs-replace-ra-ca',
    version='0.1',
    packages=['replace_ra_ca'],
    entry_points={
        'mkdocs.plugins': [
            'replace_ra_ca = replace_ra_ca:ReplaceRaCaPlugin',
        ],
    },
)
