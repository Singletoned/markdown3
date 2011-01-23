# -*- coding: utf-8 -*-

import pegger as pg

def body():
    return pg.Many(
        title_level_2,
        title_level_1,
        numbered_bullet,
        paragraph,
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

def paragraph():
    return (
        pg.Ignore("\n"),
        pg.Many(
            plain,
            emphasis,
            link,
            code),
        pg.Ignore("\n"))

def title_level_1():
    return (
        pg.Ignore("\n#"),
        pg.Words(),
        pg.Ignore(
            (pg.Optional("#"),
             "\n")))

def title_level_2():
    return (
        pg.Ignore("\n##"),
        pg.Words(),
        pg.Ignore(
            (pg.Optional("##"),
             "\n")))

def digits():
    return pg.Words(letters="1234567890")

def numbered_bullet():
    return (
        pg.Ignore("\n"),
        pg.Ignore(digits),
        pg.Ignore(". "),
        pg.Words(),
        pg.Ignore("\n"))


def parse(text):
    return pg.parse_string(text, body)
