# -*- coding: utf-8 -*-

import itertools, functools

def make_tagname_decorator(tagname_lookups):
    def tagname_decorator(tagname):
        def inner(func):
            func_name = func.__name__
            tagname_lookups[func_name] = tagname
            return func
        return inner
    return tagname_decorator

def make_htmlise_decorator(htmliser_funcs):
    def htmliser_decorator(htmliser_func):
        def inner(func):
            func_name = func.__name__
            htmliser_funcs[func_name] = htmliser_func
            return func
        return inner
    return htmliser_decorator

def do_render(data, tagname_lookups, htmliser_funcs):
    if isinstance(data, basestring):
        return [data]
    else:
        head, rest = data[0], data[1:]
        func = htmliser_funcs[head]
        return func(head, rest, tagname_lookups, htmliser_funcs)

def indent_tags(data):
    "Indent the tags"
    result = []
    for item in data:
        result.append("  "+item)
    return result

def make_block(head, rest, tagname_lookups, htmliser_funcs):
    tag = tagname_lookups[head]
    start_tag = "<%s>" % tag
    end_tag = "</%s>" % tag
    content = []
    if (isinstance(rest[0], basestring)):
        single_line = True
    else:
        single_line = False
    content = []
    for item in rest:
        content.extend(do_render(item, tagname_lookups, htmliser_funcs))
    if single_line:
        content = ["".join(content)]
    content = indent_tags(content)
    return [start_tag] + content + [end_tag]

def make_block_with_linebreak(head, rest, tagname_lookups, htmliser_funcs):
    return make_block(head, rest, tagname_lookups, htmliser_funcs) + [""]

def make_span(head, rest, tagname_lookups, htmliser_funcs):
    tag = tagname_lookups[head]
    if tag:
        start_tag = "<%s>" % tag
        end_tag = "</%s>" % tag
    else:
        start_tag = ""
        end_tag = ""
    content = []
    for item in rest:
        content.extend(do_render(item, tagname_lookups, htmliser_funcs))
    content = "".join(content)
    return ["%s%s%s" % (start_tag, content, end_tag)]

def make_span_with_linebreak(head, rest, tagname_lookups, htmliser_funcs):
    return make_span(head, rest, tagname_lookups, htmliser_funcs) + [""]

def make_void_element(head, rest, tagname_lookups, htmliser_funcs):
    tag = tagname_lookups[head]
    tag = "<%s/>" % tag
    return [tag]

def make_void_element_with_linebreak(head, rest, tagname_lookups, htmliser_funcs):
    return make_void_element(head, rest, tagname_lookups, htmliser_funcs) + [""]

def make_tagless(head, rest, tagname_lookups, htmliser_funcs):
    content = []
    for item in rest:
        content.extend(do_render(item, tagname_lookups, htmliser_funcs))
    return content

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

def render_void_element(head, rest, with_linebreak=False):
    "Render something as a void element, ignoring contents"
    tag_name = tags[head]
    if with_linebreak:
        yield "<%s/>\n" % tag_name
    else:
        yield "<%s/>" % tag_name

tag_dispatchers = dict(
    heading_1=functools.partial(render_spans, with_linebreak=True),
    heading_2=functools.partial(render_spans, with_linebreak=True),
    horizontal_rule=functools.partial(render_void_element, with_linebreak=True),
    unordered_list=functools.partial(render_block, with_linebreak=True),
    unordered_list_nested=render_block,
    unordered_bullet=render_block,
    ordered_list=functools.partial(render_block, with_linebreak=True),
    ordered_list_nested=render_block,
    ordered_bullet=render_block,
    body=render_tagless,
    emphasis=render_spans,
    paragraph=functools.partial(render_spans, with_linebreak=False))

def generate_html(data):
    "Convert a tree to flattened html"
    data = iter(data)
    head = data.next()
    dispatcher = tag_dispatchers[head]
    for item in dispatcher(head, data):
        yield item
