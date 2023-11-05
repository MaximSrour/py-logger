from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="logger",
    version="0.0.2",
    packages=find_packages(),
    author="Maxim Srour",
    author_email="maxim.srour@gmail.com",
    description="A simple logger package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='your package keywords',
    url="https://github.com/MaximSrour/logger",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # Any dependencies you have, e.g., 'requests >= 2.19.1',
    ]
)
