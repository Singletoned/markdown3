# -*- coding: utf-8 -*-

import pegger as pg

def body():
    return pg.Many(
        title_level_2,
        title_level_1,
        ordered_list,
        unordered_list,
        code_block,
        paragraph,
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
        pg.Ignore(
            pg.Optional(
                pg.Many("\n"))),
        span_text)

def title_level_1():
    return (
        pg.Ignore(
            pg.Many("\n")),
        pg.Ignore("#"),
        pg.Words(),
        pg.Ignore(
            (pg.Optional("#"),
             "\n")))

def title_level_2():
    return (
        pg.Ignore(
            pg.Many("\n")),
        pg.Ignore("##"),
        pg.Words(),
        pg.Ignore(
            (pg.Optional("##"),
             "\n")))

def digits():
    return pg.Words(letters="1234567890")

def ordered_list():
    return (
        pg.Ignore(
            pg.Optional(
                pg.Many("\n"))),
        pg.Indented(
        (
        numbered_bullet,
        pg.Optional(
            pg.Many(
                numbered_bullet,
                    ordered_list))),
        optional=True))

def numbered_bullet():
    return (
        pg.Ignore(
            pg.Optional(
                pg.Many("\n"))),
        pg.Ignore(digits),
        pg.Ignore(". "),
        span_text)

def unordered_list():
    return (
        pg.Ignore(
            pg.Optional(
                pg.Many("\n"))),
        pg.Indented(
        (
        bullet,
        pg.Optional(
            pg.Many(
                bullet,
                unordered_list))),
        optional=True))

def bullet():
    return (
        pg.Ignore(
            pg.Optional(
                pg.Many("\n"))),
        pg.Ignore("* "),
        span_text)

span_text = pg.Many(
    plain,
    emphasis,
    link,
    code),

def code_line():
    return pg.Escaped(pg.Not("\n"))

code_paragraph = (
    pg.Ignore(
        pg.Optional(
            pg.Many("\n"))),
    pg.Many(
        code_line))

def code_block():
    return (
        pg.Ignore(
            pg.Optional(
                pg.Many("\n"))),
        pg.Indented(
            code_paragraph))

def parse(text):
    return pg.parse_string(text, body)

def to_html(data):
    return pg.htmlise(pg.parse_string(data, body))
