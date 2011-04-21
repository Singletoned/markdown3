# -*- coding: utf-8 -*-


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
    unordered_list="ul",
    unordered_list_nested="ul",
    unordered_bullet="li")

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

def render_spans(data):
    "Render the spans"
    data = iter(data)
    tag_name = data.next()
    current_text = ["<%s>" % tag_name]
    for item in data:
        if isinstance(item, basestring):
            current_text.append(item)
        else:
            for sub_item in render_spans(item):
                current_text.append(sub_item)
    current_text.append("</%s>" % tag_name)
    yield "".join(current_text)

def generate_html(data):
    "Convert a tree to flattened html"
    data = iter(data)
    tag_name = data.next()
    content = "".join(data)
    yield "<%s>%s</%s>" % (tag_name, content, tag_name)
