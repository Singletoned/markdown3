# -*- coding: utf-8 -*-

import string

import pegger as pg
import htmlise

tagname_lookups = dict()
tagname = htmlise.make_tagname_decorator(tagname_lookups)
htmliser_funcs = dict()
htmliser = htmlise.make_htmlise_decorator(htmliser_funcs)


@htmliser(htmlise.make_tagless)
def body():
    return pg.Many(
        pg.OneOf(
            linebreaks,
            heading_1,
            heading_2))

# def body():
#     return pg.Many(
#         linebreaks,
#         horizontal_rule,
#         title_level_2,
#         title_level_1,
#         ordered_list,
#         unordered_list,
#         code_block,
#         paragraph,
#         blockquote,
#         )

# def plain():
#     return pg.Words(string.lowercase+string.uppercase+string.digits+"., :")

def emphasis():
    return pg.AllOf(
        pg.Ignore('*'),
        multiline_words,
        pg.Ignore('*'))

multiline_words = pg.AllOf(
    pg.Words(string.lowercase+string.uppercase+string.digits+"., :"),
    pg.Optional(
        pg.Many(
            pg.AllOf(
                pg.Ignore("\n"),
                pg.Insert(" "),
                pg.Words(string.lowercase+string.uppercase+string.digits+"., :")))))

characters = pg.Words(string.lowercase+string.uppercase+string.digits+".,:")

words = pg.Join(
    pg.AllOf(
        pg.Many(
            characters),
        pg.Optional(
            pg.Many(
                pg.AllOf(
                    pg.Many(" "),
                    pg.Many(
                        characters))))))

span = pg.Many(
    pg.OneOf(
        words,
        emphasis,
        " "
        )
    )

def paragraph():
    return span

def unordered_bullet():
    return pg.AllOf(
        pg.Ignore("*"),
        pg.Ignore(" "),
        span,
        pg.Optional(
            pg.AllOf(
                pg.Ignore("\n"),
                unordered_list_nested)))

def _multiple_bullets(bullet_type):
    return pg.AllOf(
        bullet_type,
        pg.Optional(
            pg.Many(
                pg.AllOf(
                    pg.Ignore("\n"),
                    bullet_type))))

def unordered_list():
    return pg.Indented(
        _multiple_bullets(unordered_bullet),
        optional=True)

def unordered_list_nested():
    return pg.Indented(
        _multiple_bullets(unordered_bullet),
        optional=False)

def ordered_bullet():
    return pg.AllOf(
        pg.Ignore(
            pg.AllOf(
                pg.Words(letters="0123456789"),
                ". ")),
        span,
        pg.Optional(
            pg.AllOf(
                pg.Ignore("\n"),
                ordered_list_nested)))

def ordered_list():
    return pg.Indented(
        _multiple_bullets(ordered_bullet),
        optional=True)

def ordered_list_nested():
    return pg.Indented(
        _multiple_bullets(ordered_bullet),
        optional=False)

def linebreaks():
    return pg.Ignore(
        pg.Many("\n"))

@htmliser(htmlise.make_span)
@tagname("h1")
def heading_1():
    return pg.AllOf(
        pg.Ignore("# "),
        words,
        pg.Optional(
            pg.Ignore(" #")))

@htmliser(htmlise.make_span)
@tagname("h2")
def heading_2():
    return pg.AllOf(
        pg.Ignore("## "),
        words,
        pg.Optional(
            pg.Ignore(" ##")))


# def plain():
#     return multiline_words

# def link():
#     return pg.AllOf(link_text, link_url)

# def link_text():
#     return pg.AllOf(
#         pg.Ignore("["),
#         pg.Join(
#             pg.Many(
#                 pg.Not("]"))),
#         pg.Ignore("]"))

# def link_url():
#     return pg.AllOf(
#         pg.Ignore("("),
#         pg.Join(
#             pg.Many(
#                 pg.Not(")"))),
#         pg.Ignore(")"))

# def code():
#     return pg.AllOf(
#         pg.Ignore("`"),
#         pg.Join(
#             pg.Many(
#                 pg.Not("`"))),
#         pg.Ignore("`"))

# def paragraph():
#     return pg.AllOf(
#         span_text)

# linebreaks = pg.Ignore(
#     pg.Many("\n"))

# def title_level_1():
#     return pg.AllOf(
#         pg.Ignore("# "),
#         pg.Words(),
#         pg.Ignore(
#             pg.AllOf(
#                 pg.Optional(" "),
#                 pg.Optional("#"),
#                 "\n")))

# def title_level_2():
#     return pg.AllOf(
#         pg.Ignore("## "),
#         pg.Words(),
#         pg.Ignore(
#             pg.AllOf(
#                 pg.Optional(" "),
#                 pg.Optional("##"),
#                 "\n")))

# def digits():
#     return pg.Words(letters="1234567890")

# def ordered_list():
#     return pg.OneOf(
#         _ordered_list_without_paragraphs,
#         _ordered_list_with_paragraphs,
#         _ordered_list_with_single_bullet
#         )

# def ordered_list_nested():
#     return pg.OneOf(
#         _ordered_list_without_paragraphs_nested,
#         _ordered_list_with_paragraphs_nested,
#         _ordered_list_with_single_bullet_nested,
#         )

# def numbered_bullet_without_paragraph():
#     return pg.AllOf(
#         pg.Ignore(digits),
#         pg.Ignore("."),
#         pg.Ignore(
#             pg.OneOf(" ", "\t")),
#         span_text)

# def numbered_bullet_with_paragraph():
#     return pg.Indented(
#         pg.AllOf(
#             paragraph,
#             pg.Optional(
#                 pg.AllOf(
#                     linebreaks,
#                     paragraph))),
#         initial_indent=pg.AllOf(
#             pg.Optional(
#                 linebreaks),
#             pg.OneOf(
#                 pg.AllOf(
#                     pg.Ignore(digits),
#                     pg.Ignore("."),
#                     pg.Many('\t')),
#                 pg.AllOf(
#                     digits,
#                     ".",
#                     " "))))

# def _ordered_list_with_single_bullet():
#     return pg.Indented(
#         numbered_bullet_without_paragraph,
#         optional=True)

# def _ordered_list_with_single_bullet_nested():
#     return pg.Indented(
#         numbered_bullet_without_paragraph,
#         optional=False)

# def _ordered_list_template(bullet_type, spacing, optional=True):
#     return pg.Indented(
#         pg.AllOf(
#             bullet_type,
#             pg.Many(
#                 pg.AllOf(
#                     pg.Ignore(
#                         spacing),
#                     pg.OneOf(
#                         bullet_type,
#                         ordered_list_nested,
#                         unordered_list)))),
#         optional=optional)

# def _ordered_list_without_paragraphs():
#     return _ordered_list_template(
#         bullet_type=numbered_bullet_without_paragraph,
#         spacing="\n")

# def _ordered_list_without_paragraphs_nested():
#     return _ordered_list_template(
#         bullet_type=numbered_bullet_without_paragraph,
#         spacing="\n",
#         optional=False)

# def _ordered_list_with_paragraphs():
#     return _ordered_list_template(
#         bullet_type=numbered_bullet_with_paragraph,
#         spacing="\n\n")

# def _ordered_list_with_paragraphs_nested():
#     return _ordered_list_template(
#         bullet_type=numbered_bullet_with_paragraph,
#         spacing="\n\n",
#         optional=False)

# def unordered_list():
#     return pg.OneOf(
#         _unordered_list_without_paragraphs,
#         _unordered_list_with_paragraphs,
#         _unordered_list_with_single_bullet
#         )

# def _unordered_list_with_single_bullet():
#     return pg.Indented(
#         bullet_without_paragraph,
#         optional=True)

# def _unordered_list_template(bullet_type, spacing):
#     return pg.Indented(
#         pg.AllOf(
#             bullet_type,
#             pg.Many(
#                 pg.AllOf(
#                     pg.Ignore(
#                         spacing),
#                     pg.OneOf(
#                         bullet_type,
#                         unordered_list,
#                         ordered_list)))),
#         optional=True)

# def _unordered_list_without_paragraphs():
#     return _unordered_list_template(
#         bullet_type=bullet_without_paragraph,
#         spacing="\n")

# def _unordered_list_with_paragraphs():
#     return _ordered_list_template(
#         bullet_type=bullet_with_paragraph,
#         spacing="\n\n")

# def bullet_without_paragraph():
#     return pg.AllOf(
#         pg.Ignore(
#             pg.OneOf("*", "+", "-")),
#         pg.Ignore(
#             pg.OneOf(" ", "\t")),
#         span_text)

# def bullet_with_paragraph():
#     return pg.AllOf(
#         pg.Ignore(
#             pg.OneOf("*", "+", "-")),
#         pg.Ignore(
#             pg.OneOf(" ", "\t")),
#         paragraph)

# span_text = pg.Many(
#     plain,
#     emphasis,
#     link,
#     code)

# def code_line():
#     return pg.Escaped(
#         pg.Join(
#             pg.Many(
#                 pg.Not("\n"))))

# code_paragraph = pg.AllOf(
#     pg.Ignore(
#         pg.Optional(
#             pg.Many("\n"))),
#     pg.Many(
#         code_line))

# def code_block():
#     return pg.AllOf(
#         pg.Indented(
#             code_paragraph))

# def horizontal_rule():
#     return pg.AllOf(
#         pg.OneOf(
#             "---",
#             "___",
#             "***",
#             "- - -",
#             "_ _ _",
#             "* * *"),
#         pg.Optional(
#             pg.Ignore(
#                 pg.Many(
#                     pg.Not("\n")))))

# def blockquote():
#     return pg.AllOf(
#         pg.Ignore('> '),
#         paragraph
#         )


lookups = {
    # '': None,
    # 'nested_list': "ol",
    # 'ordered_list': "ol",
    # 'ordered_list_nested': "ol",
    # 'list_item': "li",
    # 'body': "body",
    # 'numbered_bullet_with_paragraph': "li",
    # 'numbered_bullet_without_paragraph': "li",
    # 'plain': None,
    # 'emphasis': "strong",
    # 'code': "code",
    # 'link_text': None,
    # 'link_url': None,
    # 'link': "a",
    # 'paragraph': "p",
    # 'title_level_1': "h1",
    # 'title_level_2': "h2",
    # 'code_block': "code",
    # 'code_line': None,
    # 'unordered_list': "ul",
    # 'bullet_with_paragraph': "li",
    # 'bullet_without_paragraph': "li",
    # 'horizontal_rule': "hr",
    # 'blockquote': "blockquote",
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

def make_void_element_with_linebreak(head, rest):
    return make_void_element(head, rest) + [""]

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
    return [start_tag] + content + [end_tag] + [""]

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

def make_span_with_linebreak(head, rest):
    return make_span(head, rest) + [""]

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
    # 'list_item': make_span,
    # 'emphasis': make_span,
    # 'ordered_list': make_block,
    # 'ordered_list_nested': make_block,
    # 'code': make_span,
    # '': make_tagless,
    # 'nested_list': make_block,
    # 'plain': make_span,
    # 'link': make_anchor,
    # 'link_text': make_span,
    # 'body': make_tagless,
    # 'numbered_bullet_with_paragraph': make_span,
    # 'numbered_bullet_without_paragraph': make_span,
    # 'paragraph': make_span_with_linebreak,
    # 'title_level_1': make_span_with_linebreak,
    # 'title_level_2': make_span_with_linebreak,
    # 'code_block': make_block,
    # 'code_line': make_span,
    # 'unordered_list': make_block,
    # 'bullet_with_paragraph': make_span,
    # 'bullet_without_paragraph': make_span,
    # 'horizontal_rule': make_void_element_with_linebreak,
    # 'blockquote': make_block,
    }

# def do_render(data):
#     if isinstance(data, basestring):
#         return [data]
#     else:
#         head, rest = data[0], data[1:]
#         func = tag_funcs[head]
#         return func(head, rest)

# def htmlise(node, depth=0):
#     return "\n".join(do_render(node))

def parse(text, pattern=body, with_rest=False):
    if not with_rest:
        return pg.parse_string(text, pattern)
    else:
        return pg.do_parse(text, pattern)

# def to_html(text, pattern=body):
#     if not text.endswith("\n\n"):
#         text = text + "\n\n"
#     return htmlise(pg.parse_string(text, pattern)).strip()

# def htmlise(node, depth=0):
#     return "\n".join(do_render(node))

def to_html(text, pattern=body):
    data = pg.parse_string(text, pattern)
    return "\n".join(htmlise.do_render(data, tagname_lookups, htmliser_funcs))
