from setuptools import setup, find_packages

with open('requirements.txt') as f:
    packages_required = f.read().splitlines()

setup(
    name='required_packages',
    version='1.0',
    packages=find_packages(),
    install_requires=packages_required
)