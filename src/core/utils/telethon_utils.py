# -*- coding: utf-8 -*-

def adapt_link(link: str) -> str:
    return link.removeprefix('https://t.me/').removeprefix('@').removesuffix('/')
