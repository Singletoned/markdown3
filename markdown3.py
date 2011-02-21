# -*- coding: utf-8 -*-

import pegger as pg

def body():
    return pg.Many(
        code,
        title_level_2,
        title_level_1,
        ordered_list,
        paragraph,
        code_block,
        plain,
        emphasis,
        link,
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
        span_text,
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

def ordered_list():
    return (
        numbered_bullet,
        pg.Optional(
            pg.Many(
                numbered_bullet,
                pg.Indented(
                    ordered_list))))

def numbered_bullet():
    return (
        pg.Ignore(
            pg.Optional("\n")),
        pg.Ignore(digits),
        pg.Ignore(". "),
        span_text)

span_text = pg.Many(
    plain,
    emphasis,
    link,
    code),

def code_line():
    return pg.Not("\n")

code_paragraph = (
    pg.Ignore("\n"),
    pg.Many(
        code_line))

def code_block():
    return pg.Indented(code_paragraph)

def parse(text):
    return pg.parse_string(text, body)

def to_html(data):
    return pg.htmlise(pg.parse_string(data, body))
