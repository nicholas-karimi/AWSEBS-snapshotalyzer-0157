from setuptools import setup

setup(
    name='snapshotalyzer-0157',
    version='0.1',
    author='Nicholas Karimi',
    author_email='nicholaskarimi.dev@gmail.com',
    description='SanpshotAlyzer 0157 is a tool that manages AWS EC2 snapshots',
    license='GPLV3+',
    packages=['snappy'],
    url='https://github.com/nicholas-karimi/AWSEBS-snapshotalyzer-0157,
    install_requires=[
        'click',
        'boto3'
    ],
    entry_point='''
    [console_scripts]
    snappy=snappy.snappy:cli
        ''',
    )
