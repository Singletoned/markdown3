# -*- coding: utf-8 -*-

import pyparsing as pp

def parse(text):
    strong_start = pp.Literal("**").setParseAction(pp.replaceWith("<strong>"))
    strong_end = pp.Literal("**").setParseAction(pp.replaceWith("</strong>"))
    strong_phrase = strong_start + pp.SkipTo(strong_end) + strong_end
    em_start = pp.Literal("*").setParseAction(pp.replaceWith("<em>"))
    em_end = pp.Literal("*").setParseAction(pp.replaceWith("</em>"))
    em_phrase = em_start + pp.SkipTo(em_end) + em_end
    sentence = pp.MatchFirst([strong_phrase, em_phrase])
    return sentence.transformString(text)
