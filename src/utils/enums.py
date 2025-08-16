from enum import Enum


class Mode(Enum):
    DEV = 1
    PROD = 2


class Source(Enum):
    API = 1
    DATABASE = 2
