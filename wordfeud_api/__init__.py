"""
Wordfeud API Client

A Python client for the Wordfeud API.
"""

from .wordfeud import (
    Wordfeud,
    WordfeudException,
    WordfeudLogInException,
    WordfeudClientException,
    WordfeudHttpException,
    WordfeudJsonException
)

__version__ = "0.2.0"
__author__ = "mallpunk"
__description__ = "Python API client for Wordfeud"

__all__ = [
    "Wordfeud",
    "WordfeudException", 
    "WordfeudLogInException",
    "WordfeudClientException",
    "WordfeudHttpException",
    "WordfeudJsonException"
] 