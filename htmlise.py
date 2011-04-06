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
