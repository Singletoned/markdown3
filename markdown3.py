# -*- coding: utf-8 -*-

import pegger as pg

def body():
    return pg.Many(
        horizontal_rule,
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
    return pg.AllOf(
        pg.Ignore('*'),
        pg.Words(),
        pg.Ignore('*'))

def link():
    return pg.AllOf(link_text, link_url)

def link_text():
    return pg.AllOf(
        pg.Ignore("["),
        pg.Words(),
        pg.Ignore("]"))

def link_url():
    return pg.AllOf(
        pg.Ignore("("),
        pg.Not(")"),
        pg.Ignore(")"))

def code():
    return pg.AllOf(
        pg.Ignore("`"),
        pg.Not("`"),
        pg.Ignore("`"))

def paragraph():
    return pg.AllOf(
        linebreaks,
        span_text)

def title_level_1():
    return pg.AllOf(
        pg.Ignore(
            pg.Many("\n")),
        pg.Ignore("#"),
        pg.Words(),
        pg.Ignore(
            pg.AllOf(
                pg.Optional("#"),
                "\n")))

def title_level_2():
    return pg.AllOf(
        pg.Ignore(
            pg.Many("\n")),
        pg.Ignore("##"),
        pg.Words(),
        pg.Ignore(
            pg.AllOf(
                pg.Optional("##"),
                "\n")))

def digits():
    return pg.Words(letters="1234567890")

def ordered_list():
    return pg.AllOf(
        linebreaks,
        pg.Indented(
            pg.AllOf(
                numbered_bullet,
                pg.Optional(
                    pg.Many(
                        numbered_bullet,
                        ordered_list,
                        unordered_list))),
            optional=True))

def numbered_bullet():
    return pg.AllOf(
        linebreaks,
        pg.Ignore(digits),
        pg.Ignore(". "),
        span_text)

def unordered_list():
    return pg.AllOf(
        linebreaks,
        pg.Indented(
            pg.AllOf(
                bullet,
                pg.Optional(
                    pg.Many(
                        bullet,
                        unordered_list,
                        ordered_list))),
            optional=True))

def bullet():
    return pg.AllOf(
        linebreaks,
        pg.Ignore("* "),
        span_text)

span_text = pg.Many(
    plain,
    emphasis,
    link,
    code)

def code_line():
    return pg.Escaped(pg.Not("\n"))

code_paragraph = pg.AllOf(
    pg.Ignore(
        pg.Optional(
            pg.Many("\n"))),
    pg.Many(
        code_line))

def code_block():
    return pg.AllOf(
        linebreaks,
        pg.Indented(
            code_paragraph))

def horizontal_rule():
    return pg.AllOf(
        linebreaks,
        pg.Ignore("---"),
        ""
        )

linebreaks = pg.Ignore(
    pg.Optional(
        pg.Many("\n")))

def parse(text):
    return pg.parse_string(text, body)

def to_html(data):
    return pg.htmlise(pg.parse_string(data, body))
