# -*- coding: utf-8 -*-

import pegger as pg

def body():
    return pg.Many(
        plain,
        emphasis,
        link,
        code,
        )

def plain():
    return pg.Words()

def emphasis():
    return (
        pg.Ignore('*'),
        pg.Words(),
        pg.Ignore('*'))

def link():
    return (link_text, link_url)

def link_text():
    return (
        pg.Ignore("["),
        pg.Words(),
        pg.Ignore("]"))

def link_url():
    return (
        pg.Ignore("("),
        pg.Not(")"),
        pg.Ignore(")"))

def code():
    return (
        pg.Ignore("`"),
        pg.Not("`"),
        pg.Ignore("`"))

def parse(text):
    return pg.parse_string(text, body)
