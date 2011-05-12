# -*- coding: utf-8 -*-

import itertools, functools

tags = dict(
    heading_1="h1",
    heading_2="h2",
    unordered_list="ul",
    unordered_list_nested="ul",
    unordered_bullet="li",
    ordered_list="ol",
    ordered_list_nested="ol",
    ordered_bullet="li",
    paragraph="p",
    emphasis="strong",
    body="body",
    span="span",
    link="a",
    horizontal_rule="hr")

def convert_tags(data):
    "Convert parser element names to tags"
    data = iter(data)
    tag = tags[data.next()]
    yield tag
    for item in data:
        if isinstance(item, basestring):
            yield item
        else:
            yield convert_tags(item)

def indent(data):
    for item in data:
        yield "  %s" % item

block_tags = set([
    "ul", "li", "p"
    ])

def _render_contents(data):
    current_text = []
    for item in data:
        if isinstance(item, basestring):
            current_text.append(item)
        else:
            item = iter(item)
            sub_head = item.next()
            dispatcher = tag_dispatchers[sub_head]
            tag = tags[sub_head]
            if tag in block_tags:
                if current_text:
                    yield "".join(current_text)
                    current_text = []
                for sub_item in dispatcher(sub_head, item):
                    yield sub_item
            else:
                for sub_item in dispatcher(sub_head, item):
                    current_text.append(sub_item)
    if current_text:
        yield "".join(current_text)

def render_spans(head, rest, with_linebreak=False):
    "Render the spans"
    data = iter(rest)
    tag_name = tags[head]
    items = ["<%s>" % tag_name]
    items.extend(_render_contents(data))
    items.append("</%s>" % tag_name)
    if with_linebreak:
        items.append("\n")
    result = "".join(items)
    yield result

def render_block(head, rest, with_linebreak=False, with_inline_contents=False):
    "Render the block"
    data = iter(rest)
    tag_name = tags[head]
    yield "<%s>" % tag_name
    for item in indent(_render_contents(data)):
        yield item
    if with_linebreak:
        yield "</%s>\n" % tag_name
    else:
        yield "</%s>" % tag_name

def render_tagless(head, rest):
    "Render something without tags"
    data = iter(rest)
    for item in data:
        item = iter(item)
        sub_head = item.next()
        dispatcher = tag_dispatchers[sub_head]
        for sub_item in dispatcher(sub_head, item):
            yield sub_item
        yield ""

def render_void_element(head, rest, with_linebreak=False):
    "Render something as a void element, ignoring contents"
    tag_name = tags[head]
    if with_linebreak:
        yield "<%s/>\n" % tag_name
    else:
        yield "<%s/>" % tag_name

def render_link(head, rest):
    "Render a link.  `rest` is a list of key, value pairs"
    data = dict(rest)
    template = '''<a href="%(link_url)s">%(link_text)s</a>'''
    yield template % data

tag_dispatchers = dict(
    heading_1=render_spans,
    heading_2=render_spans,
    horizontal_rule=render_void_element,
    unordered_list=render_block,
    unordered_list_nested=render_block,
    unordered_bullet=render_block,
    ordered_list=render_block,
    ordered_list_nested=render_block,
    ordered_bullet=render_block,
    body=render_tagless,
    emphasis=render_spans,
    link=render_link,
    paragraph=functools.partial(render_spans, with_linebreak=False))

def generate_html(data):
    "Convert a tree to flattened html"
    data = iter(data)
    head = data.next()
    dispatcher = tag_dispatchers[head]
    for item in dispatcher(head, data):
        yield item
