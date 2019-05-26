from os import path

from setuptools import setup, find_packages

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md")) as f:
    long_description = f.read()


setup(
    name="desc-db-md",
    version='0.0.1',

    description="Database Descriptor Markdown",
    long_description=long_description,
    url="https://github.com/crunchmind/desc-db-md",

    packages=find_packages(),


    # Generating the command-line tool
    entry_points={
        "console_scripts": [
            "descdbmd=descdbmd.main:main"
        ]
    },

    install_requires=['boto3']
)
