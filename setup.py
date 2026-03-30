from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='terminapy',
    version='0.0.3',
    packages=find_packages(),
    packages_data={
        "terminapy":["py.typed"],    
    },
    install_requires=[
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
