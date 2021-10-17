# -*- coding: utf-8 -*-

from enum import Enum


class Address(Enum):
    America = "NewYork"
    China = "Beijing"
    Japan = "Tokyo"


if __name__ == "__main__":
    print(Address.America.value)