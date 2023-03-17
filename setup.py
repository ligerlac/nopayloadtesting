from setuptools import find_packages, setup

setup(
    name='nopayloadtesting',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        #'htcondor',
        'requests',
        'numpy',
        'matplotlib'
        ],
)
