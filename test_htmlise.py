# -*- coding: utf-8 -*-

import unittest
import contextlib

import py.test
import mock

import pegger as pg
import markdown3 as md
import htmlise


@contextlib.contextmanager
def patch_tagname_lookups_and_htmliser_funcs():
    with mock.patch.dict(htmlise.tagname_lookups):
        with mock.patch.dict(htmlise.htmliser_funcs):
            yield

def test_register_tag():
    with patch_tagname_lookups_and_htmliser_funcs():
        @htmlise.register_func(md.make_block, "foo")
        def my_func():
            pass

        assert htmlise.htmliser_funcs == {'my_func': md.make_block}
        assert htmlise.tagname_lookups == {'my_func': "foo"}
        assert callable(my_func)


class TestDoRender(unittest.TestCase):
    """Unittests for do_render"""

    def test_string(self):
        """Test that a string returns itself in a list"""
        data = """foo"""
        expected = ['foo']
        result = htmlise.do_render(data)
        assert expected == result

    def test_list(self):
        """Test that a list is passed to a renderer"""
        with patch_tagname_lookups_and_htmliser_funcs():
            def make_foo(head, rest):
                return repr((head, rest))

            htmlise.tagname_lookups['foo'] = "footag"
            htmlise.htmliser_funcs['foo'] = make_foo

            data = ['foo', "bar"]
            expected = "('foo', ['bar'])"
            result = htmlise.do_render(data)
            assert expected == result


def test_make_block():
    with patch_tagname_lookups_and_htmliser_funcs():
        @htmlise.register_func(htmlise.make_block, "footag")
        def foo():
            pass

        data = ['foo', "bar", "baz"]
        expected = [
            "<footag>",
            "barbaz",
            "</footag>"]
        result = htmlise.make_block(data[0], data[1:])
        assert expected == result


def test_make_span():
    with patch_tagname_lookups_and_htmliser_funcs():
        @htmlise.register_func(htmlise.make_span, "footag")
        def foo():
            pass

        data = ['foo', "flibble", "flammle"]
        expected = ["<footag>flibbleflammle</footag>"]
        result = htmlise.make_span(data[0], data[1:])
        assert expected == result

    # data = [
    #     'plain',
    #     "A paragraph with ",
    #     ['emphasis', "some bold"],
    #     " and ",
    #     ['code', "code"],
    #     " in it"]
    # expected = ["A paragraph with <strong>some bold</strong> and <code>code</code> in it"]
    # result = md.make_span(data[0], data[1:])
    # assert expected == result


# def test_make_void_element():
#     data = ['horizontal_rule', ""]
#     expected = ['<hr/>']
#     result = md.make_void_element(data[0], data[1:])
#     assert expected == result

# def test_make_void_element_with_linebreak():
#     data = ['horizontal_rule', ""]
#     expected = ['<hr/>', ""]
#     result = md.make_void_element_with_linebreak(data[0], data[1:])
#     assert expected == result

# def test_make_span_with_linebreak():
#     data = [
#         'title_level_1',
#         "FooBar"]
#     expected = ["<h1>FooBar</h1>", ""]
#     result = md.make_span_with_linebreak(data[0], data[1:])
#     assert expected == result

# def test_do_render():
#     data = [
#         'list_item',
#         ['emphasis',
#          "some bold"]]
#     expected = [
#         "<li><strong>some bold</strong></li>"]
#     result = md.do_render(data)
#     assert expected == result

# def test_htmlise():
#     data = ['list_item', "A bullet"]
#     expected = """
# <li>A bullet</li>""".strip()
#     result = md.htmlise(data)
#     assert expected == result

#     data = [
#         'ordered_list',
#         ['list_item', "A bullet"]]
#     expected = """
# <ol>
#   <li>A bullet</li>
# </ol>""".strip()
#     result = md.htmlise(data).strip()
#     assert expected == result

#     data = [
#         'list_item',
#         ['plain',
#          "A bullet with some ",
#          ['emphasis',
#           "bold"],
#          " in it"]]
#     expected = """
# <li>A bullet with some <strong>bold</strong> in it</li>""".strip()
#     result = md.htmlise(data).strip()
#     assert expected == result


# def test_htmlise_2():
#     data = """
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

#     result = md.to_html(data).strip()
#     assert result == expected_html


# def test_htmlise_link():
#     data = [
#         'link',
#         ['link_text', "a link to Google"],
#         ['link_url',
#          "http://www.google.com"]]

#     expected_html = ['''
#     <a href="http://www.google.com">a link to Google</a>
#     '''.strip()]
#     result = md.make_anchor(data[0], data[1:])
#     assert expected_html == result

#     expected_html = '''
#     <a href="http://www.google.com">a link to Google</a>
#     '''.strip()
#     result = md.htmlise(data)
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

#     data = """
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

#     result = pg.parse_string(data, ordered_list)
#     assert expected == result
