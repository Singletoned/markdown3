# -*- coding: utf-8 -*-

import pegger as pg

def body():
    return pg.Many(plain)

def plain():
    return pg.Words()

def parse(text):
    return pg.parse_string(text, body)
