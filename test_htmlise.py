# -*- coding: utf-8 -*-

import unittest
import contextlib

import py.test
import mock

import pegger as pg
import markdown3 as md
import htmlise

def listify(data):
    if isinstance(data, basestring):
        return data
    else:
        return [listify(item) for item in data]


class TestConvertTags(unittest.TestCase):
    """Unittests for convert_tags"""

    def test_nested_list(self):
        """Test that convert tags handles a nested list"""
        datum = [
            'unordered_list',
            ['unordered_bullet',
             "list 1, bullet 1",
             ['unordered_list_nested',
              ['unordered_bullet',
               "list 2, bullet 1"],
              ['unordered_bullet',
               "list 2, bullet 2"]]]]
        expected = [
            'ul',
            ['li',
             "list 1, bullet 1",
             ['ul',
              ['li',
               "list 2, bullet 1"],
              ['li',
               "list 2, bullet 2"]]]]
        result = listify(htmlise.convert_tags(datum))
        assert expected == result


def test_indent():
    "Test that indent indents things"
    datum = [
        "foo",
        "bar"]
    expected = [
        "  foo",
        "  bar"]
    result = list(htmlise.indent(datum))
    assert expected == result


class TestRenderSpans(unittest.TestCase):
    """Unittests for render_spans"""

    def test_simple(self):
        """test simple"""
        def do_test(with_linebreak):
            datum = [
                'span',
                "flooble",
                " ",
                "flobble"]
            expected = ["<span>flooble flobble</span>"]
            if with_linebreak:
                expected[-1] = expected[-1] + "\n"
            result = listify(
                htmlise.render_spans(
                    datum[0],
                    datum[1:],
                    with_linebreak=with_linebreak))
            assert expected == result

        for with_linebreak in [True, False]:
            do_test(with_linebreak)

    def test_with_tags(self):
        """Test with tags"""
        def do_test(with_linebreak):
            datum = [
                'span',
                "flooble",
                " ",
                ['emphasis',
                 "booble"],
                " ",
                "flim flam"]
            expected = [
                "<span>flooble <strong>booble</strong> flim flam</span>"]
            if with_linebreak:
                expected[-1] = expected[-1] + "\n"
            result = listify(
                htmlise.render_spans(
                    datum[0],
                    datum[1:],
                    with_linebreak=with_linebreak))
            assert expected == result

        for with_linebreak in [True, False]:
            do_test(with_linebreak)

    def test_nested(self):
        """Test with nested tags"""
        def do_test(with_linebreak):
            datum = [
                'span',
                "flooble",
                " ",
                ['emphasis',
                 "booble",
                 " ",
                 "bobble"],
                " ",
                "flim flam"]
            expected = [
                "<span>flooble <strong>booble bobble</strong> flim flam</span>"]
            if with_linebreak:
                expected[-1] = expected[-1] + "\n"
            result = listify(
                htmlise.render_spans(
                    datum[0],
                    datum[1:],
                    with_linebreak=with_linebreak))
            assert expected == result

        for with_linebreak in [True, False]:
            do_test(with_linebreak)


class TestRenderBlock(unittest.TestCase):
    """Unittests for render_block"""

    def test_simple(self):
        """simple test"""
        def do_test(with_linebreak):
            datum = [
                'unordered_list',
                ['unordered_bullet',
                 "flibble"],
                ['unordered_bullet',
                 "flobble"]]
            expected = [
                "<ul>",
                "  <li>",
                "    flibble",
                "  </li>",
                "  <li>",
                "    flobble",
                "  </li>",
                "</ul>"]
            if with_linebreak:
                expected[-1] = expected[-1] + "\n"
            result = listify(
                htmlise.render_block(
                    datum[0],
                    datum[1:],
                    with_linebreak=with_linebreak))
            assert expected == result

        for with_linebreak in [True, False]:
            do_test(with_linebreak)

    def test_nested(self):
        """Test whether render_block handles nested blocks"""
        def do_test(with_linebreak):
            datum = [
                'unordered_list',
                ['unordered_bullet',
                 "flibble",
                 ['unordered_list_nested',
                  ['unordered_bullet',
                   "blibble"],
                  ['unordered_bullet',
                   "blobble"]]],
                ['unordered_bullet',
                 "flobble"]]
            expected = [
                "<ul>",
                "  <li>",
                "    flibble",
                "    <ul>",
                "      <li>",
                "        blibble",
                "      </li>",
                "      <li>",
                "        blobble",
                "      </li>",
                "    </ul>",
                "  </li>",
                "  <li>",
                "    flobble",
                "  </li>",
                "</ul>"]
            if with_linebreak:
                expected[-1] = expected[-1] + "\n"
            result = listify(
                htmlise.render_block(
                    datum[0],
                    datum[1:],
                    with_linebreak=with_linebreak))
            assert expected == result

        for with_linebreak in [True, False]:
            do_test(with_linebreak)

    def test_multiple_paragraphs(self):
        "Test that multiple paragraphs display properly"
        datum = [
            'unordered_list',
             ['unordered_bullet',
              ['paragraph',
               "bullet one, paragraph one"],
              ['paragraph',
               "bullet one, paragraph two.  Spans",
               " ",
               "multiple lines."]],
             ['unordered_bullet',
              ['paragraph',
               "bullet two"]],
             ['unordered_bullet',
              ['paragraph',
               "bullet three"]]]
        expected = [
            "<ul>",
            "  <li>",
            "    <p>bullet one, paragraph one</p>",
            "    <p>bullet one, paragraph two.  Spans multiple lines.</p>",
            "  </li>",
            "  <li>",
            "    <p>bullet two</p>",
            "  </li>",
            "  <li>",
            "    <p>bullet three</p>",
            "  </li>",
            "</ul>"]
        result = listify(
            htmlise.render_block(
                datum[0],
                datum[1:]))
        assert expected == result


def test_render_tagless():
    """Test render_tagless"""
    datum = [
        'body',
        ['paragraph',
         "flibble",
         " ",
         "flamble"]]
    expected = ["<p>flibble flamble</p>", ""]
    result = listify(htmlise.render_tagless(datum[0], datum[1:]))
    assert expected == result


class TestRenderVoidElement(unittest.TestCase):
    """Unittests for render_void_element"""

    def test_simple(self):
        """Test simplest case"""
        def do_test(with_linebreak):
            datum = ['horizontal_rule', ""]
            expected = ["<hr/>"]
            if with_linebreak:
                expected[-1] = expected[-1] + "\n"
            result = listify(
                htmlise.render_void_element(
                    datum[0],
                    datum[1:],
                    with_linebreak=with_linebreak))
            assert expected == result

        for with_linebreak in [True, False]:
            do_test(with_linebreak)

    def test_ignores_content(self):
        """Test render_void_element ignores content"""
        def do_test(with_linebreak):
            datum = [
                'horizontal_rule',
                "flibble"]
            expected = ["<hr/>"]
            if with_linebreak:
                expected[-1] = expected[-1] + "\n"
            result = listify(
                htmlise.render_void_element(
                    datum[0],
                    datum[1:],
                    with_linebreak=with_linebreak))
            assert expected == result

        for with_linebreak in [True, False]:
            do_test(with_linebreak)


class TestGenerateHTML(unittest.TestCase):
    """Unitests for generate html"""

    def test_paragraph(self):
        """Test that paragraph works"""
        datum = [
            'paragraph',
            "flibble",
            " ",
            "flamble"]
        expected = ["<p>flibble flamble</p>"]
        result = list(htmlise.generate_html(datum))
        assert expected == result

    def test_body(self):
        """Test that body works"""
        datum = [
            'body',
            ['paragraph',
             "flibble",
             " ",
             "flamble"]]
        expected = ["<p>flibble flamble</p>", ""]
        result = list(htmlise.generate_html(datum))
        assert expected == result

# def test_do_render():
#     datum = [
#         'list_item',
#         ['emphasis',
#          "some bold"]]
#     expected = [
#         "<li><strong>some bold</strong></li>"]
#     result = md.do_render(datum)
#     assert expected == result

# def test_htmlise():
#     datum = ['list_item', "A bullet"]
#     expected = """
# <li>A bullet</li>""".strip()
#     result = md.htmlise(datum)
#     assert expected == result

#     datum = [
#         'ordered_list',
#         ['list_item', "A bullet"]]
#     expected = """
# <ol>
#   <li>A bullet</li>
# </ol>""".strip()
#     result = md.htmlise(datum).strip()
#     assert expected == result

#     datum = [
#         'list_item',
#         ['plain',
#          "A bullet with some ",
#          ['emphasis',
#           "bold"],
#          " in it"]]
#     expected = """
# <li>A bullet with some <strong>bold</strong> in it</li>""".strip()
#     result = md.htmlise(datum).strip()
#     assert expected == result


# def test_htmlise_2():
#     datum = """
# * A numbered bullet
#   * A bullet in a sublist
#   * A bullet with *bold* in a sublist
# * A bullet with `code` in the first list
# """

#     expected_html = """
# <ul>
#   <li>A numbered bullet</li>
#   <ul>
#     <li>A bullet in a sublist</li>
#     <li>A bullet with <strong>bold</strong> in a sublist</li>
#   </ul>
  
#   <li>A bullet with <code>code</code> in the first list</li>
# </ul>""".strip()

#     result = md.to_html(datum).strip()
#     assert result == expected_html


# def test_htmlise_link():
#     datum = [
#         'link',
#         ['link_text', "a link to Google"],
#         ['link_url',
#          "http://www.google.com"]]

#     expected_html = ['''
#     <a href="http://www.google.com">a link to Google</a>
#     '''.strip()]
#     result = md.make_anchor(datum[0], datum[1:])
#     assert expected_html == result

#     expected_html = '''
#     <a href="http://www.google.com">a link to Google</a>
#     '''.strip()
#     result = md.htmlise(datum)
#     assert expected_html == result

# def test_numbered_bullet():
#     def numbered_bullet():
#         return pg.AllOf(
#         pg.Ignore(
#             pg.Optional(
#                 pg.Many("\n"))),
#             pg.Ignore(pg.Words(letters="1234567890")),
#             pg.Ignore(". "),
#             pg.Words())

#     def ordered_list():
#         return pg.AllOf(
#             pg.Ignore(
#                 pg.Optional(
#                     pg.Many("\n"))),
#             pg.Indented(
#                 pg.AllOf(
#                     numbered_bullet,
#                     pg.Optional(
#                         pg.Many(
#                             numbered_bullet,
#                             ordered_list))),
#                 optional=True))

#     datum = """
# 1. A numbered bullet
#   2. A bullet in a sublist
#   3. Another bullet in a sublist
# 4. Another bullet in the first list
# """

#     expected = [
#         'ordered_list',
#         ['numbered_bullet',
#          "A numbered bullet"],
#         ['ordered_list',
#          ['numbered_bullet',
#           "A bullet in a sublist"],
#          ['numbered_bullet',
#           "Another bullet in a sublist"]],
#         ['numbered_bullet',
#          "Another bullet in the first list"]]

#     result = pg.parse_string(datum, ordered_list)
#     assert expected == result
