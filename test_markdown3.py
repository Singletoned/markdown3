# -*- coding: utf-8 -*-

import markdown3

def test_body():
    data = "Hello World"
    expected = ['body', ['plain', "Hello World"]]
    result = markdown3.parse(data)
    assert expected == result

def test_emphasis():
    data = "Hello *World*"
    expected = ['body', [['plain', "Hello "], ['emphasis', "World"]]]
    result = markdown3.parse(data)
    assert expected == result

    data = "Text with *some bold* in it"
    expected = [
        'body',
        [['plain', "Text with "],
         ['emphasis', "some bold"],
         ['plain', ' in it']]]
    result = markdown3.parse(data)
    assert expected == result

def test_link():
    data = "[a link to Google](http://www.google.com)"
    expected = [
        ['link_text', "a link to Google"],
        ['link_url', "http://www.google.com"]]
    result = markdown3.pg.parse_string(data, markdown3.link)
    
    data = "Text with [a link to Google](http://www.google.com) in it"
    expected = [
        'body',
        [['plain', "Text with "],
         ['link', [
             ['link_text', "a link to Google"],
             ['link_url', "http://www.google.com"]]],
         ['plain', " in it"]]]
    result = markdown3.parse(data)
    assert expected == result

def test_code():
    data = "text with `some code` in it"
    expected = [
        'body',
        [['plain', "text with "],
         ['code', "some code"],
         ['plain', " in it"]]]
    result = markdown3.parse(data)
    assert expected == result

def test_paragraph():
    data = """
A paragraph.
"""
    expected = [
        'body',
        ['paragraph', "A paragraph."]]
    result = markdown3.parse(data)
    assert expected == result
