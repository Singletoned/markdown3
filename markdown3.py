# -*- coding: utf-8 -*-

import pegger as pg

def body():
    return pg.Many(plain, emphasis)

def plain():
    return pg.Words()

def emphasis():
    return (
        pg.Ignore('*'),
        pg.Words(),
        pg.Ignore('*'))

def parse(text):
    return pg.parse_string(text, body)
