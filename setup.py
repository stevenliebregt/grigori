from setuptools import find_packages
from setuptools import setup

setup(
    name="Grigori",
    version="1.0.1",
    url="https://github.com/stevenliebregt/grigori",
    license="MIT",
    author="Steven Liebregt",
    author_email="stevenliebregt@outlook.com",
    description="Watches a directory for file changes.",
    long_description=open("README.md").read(),
    packages=find_packages(),
)
