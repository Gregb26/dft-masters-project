from setuptools import setup, find_packages

setup(
    name="abinit_tools",
    version="0.1",
    packages=find_packages(include=["abinit_tools", "abinit_tools.*"]),
)

