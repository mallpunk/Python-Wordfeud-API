#!/usr/bin/env python3
"""
Setup script for Wordfeud API Client
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="wordfeud-api",
    version="0.2.0",
    author="mallpunk",
    author_email="",
    description="Python API client for Wordfeud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mallpunk/Python-Wordfeud-API",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    keywords="wordfeud, api, client, game",
    project_urls={
        "Bug Reports": "https://github.com/mallpunk/Python-Wordfeud-API/issues",
        "Source": "https://github.com/mallpunk/Python-Wordfeud-API",
    },
) 