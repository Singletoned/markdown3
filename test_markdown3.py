# -*- coding: utf-8 -*-

import markdown3

def test_emphasis():
    data = [
        ("*Hello*", "<em>Hello</em>"),
        ("*Hello World*", "<em>Hello World</em>"),
        ("Hello *World*", "Hello <em>World</em>"),
        ("**Hello**", "<strong>Hello</strong>"),
        ("**Hello World**", "<strong>Hello World</strong>"),
        ("Hello **World**", "Hello <strong>World</strong>"),
        ]

    for text, expected in data:
        result = markdown3.parse(text)
        assert expected == result
