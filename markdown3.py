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
        blockquote,
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
        pg.OneOf(
            "---",
            "___",
            "***",
            "- - -",
            "_ _ _",
            "* * *"),
        pg.Optional(
            pg.Ignore(
                pg.Not("\n"))))

def blockquote():
    return pg.AllOf(
        linebreaks,
        pg.Ignore('> '),
        paragraph
        )

linebreaks = pg.Ignore(
    pg.Optional(
        pg.Many("\n")))


lookups = {
    '': None,
    'nested_list': "ol",
    'ordered_list': "ol",
    'list_item': "li",
    'body': "body",
    'numbered_bullet': "li",
    'plain': None,
    'emphasis': "strong",
    'code': "code",
    'link_text': None,
    'link_url': None,
    'link': "a",
    'paragraph': "p",
    'title_level_1': "h1",
    'title_level_2': "h2",
    'code_block': "code",
    'code_line': None,
    'unordered_list': "ul",
    'bullet': "li",
    'horizontal_rule': "hr",
    'blockquote': "blockquote",
    }

def indent_tags(data):
    result = []
    for item in data:
        result.append("  "+item)
    return result

def make_void_element(head, rest):
    tag = lookups[head]
    tag = "<%s/>" % tag
    return [tag]

def make_block(head, rest):
    tag = lookups[head]
    start_tag = "<%s>" % tag
    end_tag = "</%s>" % tag
    content = []
    if (rest[0][0] == 'plain') or (isinstance(rest[0], basestring)):
        single_line = True
    else:
        single_line = False
    content = []
    for item in rest:
        content.extend(do_render(item))
    if single_line:
        content = ["".join(content)]
    content = indent_tags(content)
    return [start_tag] + content + [end_tag]

def make_span(head, rest):
    tag = lookups[head]
    if tag:
        start_tag = "<%s>" % tag
        end_tag = "</%s>" % tag
    else:
        start_tag = ""
        end_tag = ""
    content = []
    for item in rest:
        content.extend(do_render(item))
    content = "".join(content)
    return ["%s%s%s" % (start_tag, content, end_tag)]

def make_tagless(head, rest):
    content = []
    for item in rest:
        content.extend(do_render(item))
    return content

def make_anchor(head, rest):
    link_text, link_url = rest
    link_text = do_render(link_text)
    link_url = link_url[1]
    link_template = '''<a href="%s">%s</a>'''
    result = link_template % (link_url, "".join(link_text))
    return [result]

tag_funcs = {
    'list_item': make_block,
    'emphasis': make_span,
    'ordered_list': make_block,
    'code': make_span,
    '': make_tagless,
    'nested_list': make_block,
    'plain': make_span,
    'link': make_anchor,
    'link_text': make_span,
    'body': make_block,
    'numbered_bullet': make_block,
    'paragraph': make_block,
    'title_level_1': make_block,
    'title_level_2': make_block,
    'code_block': make_block,
    'code_line': make_span,
    'unordered_list': make_block,
    'bullet': make_block,
    'horizontal_rule': make_void_element,
    'blockquote': make_block,
    }

def do_render(data):
    if isinstance(data, basestring):
        return [data]
    else:
        head, rest = data[0], data[1:]
        func = tag_funcs[head]
        return func(head, rest)

def htmlise(node, depth=0):
    return "\n".join(do_render(node))

def parse(text):
    return pg.parse_string(text, body)

def to_html(data):
    return htmlise(pg.parse_string(data, body))
