# -*- coding: utf-8 -*-

htmliser_funcs = dict()
tagname_lookups = dict()


def register_func(htmliser_func, tagname):
    def inner(func):
        func_name = func.__name__
        htmliser_funcs[func_name] = htmliser_func
        tagname_lookups[func_name] = tagname
        return func
    return inner

def do_render(data):
    if isinstance(data, basestring):
        return [data]
    else:
        head, rest = data[0], data[1:]
        func = htmliser_funcs[head]
        return func(head, rest)

def make_block(head, rest):
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
        content.extend(do_render(item))
    if single_line:
        content = ["".join(content)]
    return [start_tag] + content + [end_tag]
