# -*- coding: utf-8 -*-

import path

import markdown3

td = path.path("./markdown_test_suite")


def test_markdown_test_suite():
    def do_test(datum, expected):
        result = markdown3.to_html(datum)
        assert expected == result

    for f in td.files("*.text"):
        datum = f.text()
        html_file = f.dirname() / f.namebase + ".html"
        expected = html_file.text()
        do_test(datum, expected)
