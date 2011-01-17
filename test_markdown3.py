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
