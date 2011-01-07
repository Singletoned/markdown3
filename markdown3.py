# -*- coding: utf-8 -*-

import pyparsing as pp

def parse(text):
    strong_start = pp.Literal("**").setParseAction(pp.replaceWith("<strong>"))
    strong_end = pp.Literal("**").setParseAction(pp.replaceWith("</strong>"))
    sentence = strong_start + pp.SkipTo(strong_end) + strong_end
    return sentence.transformString(text)
