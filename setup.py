from setuptools import setup, find_packages

setup(
    name='vapor-cli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'rich',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'vapor=vapor.cli:main',
        ],
    },
)