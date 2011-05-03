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
                ['strong',
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
                ['strong',
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

    def test_with_block(self):
        """Test that render_spans handles blocks"""
        def do_test(with_linebreak):
            datum = [
                'li',
                "flibble",
                ['ul',
                 ['li', "blobble"],
                 ['li', "blibble"]],
                "flammble"]
            expected = [
                "<li>flibble",
                "  <ul>",
                "    <li>blobble</li>",
                "    <li>blibble</li>",
                "  </ul>\n",
                "flammble</li>"]
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
                'ul',
                ['li',
                 "flibble"],
                ['li',
                 "flobble"]]
            expected = [
                "<ul>",
                "  <li>flibble</li>",
                "  <li>flobble</li>",
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
                'ul',
                ['li',
                 "flibble",
                 ['ul',
                  ['li',
                   "blibble"],
                  ['li',
                   "blobble"]]],
                ['li',
                 "flobble"]]
            expected = [
                "<ul>",
                "  <li>flibble",
                "    <ul>",
                "      <li>blibble</li>",
                "      <li>blobble</li>",
                "    </ul>\n",
                "  </li>",
                "  <li>flobble</li>",
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

def test_render_tagless():
    """Test render_tagless"""
    datum = [
        'body',
        ['p',
         "flibble",
         " ",
         "flamble"]]
    expected = ["<p>flibble flamble</p>\n"]
    result = listify(htmlise.render_tagless(datum[0], datum[1:]))
    assert expected == result


class TestGenerateHTML(unittest.TestCase):
    """Unitests for generate html"""

    def test_paragraph(self):
        """Test that paragraph works"""
        datum = [
            'paragraph',
            "flibble",
            " ",
            "flamble"]
        expected = ["<p>flibble flamble</p>\n"]
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
        expected = ["<p>flibble flamble</p>\n"]
        result = list(htmlise.generate_html(datum))
        assert expected == result


@contextlib.contextmanager
def patch_tagname_lookups_and_htmliser_funcs():
    with mock.patch.dict(htmlise.tagname_lookups):
        with mock.patch.dict(htmlise.htmliser_funcs):
            yield


def test_register_tag():
    tagname_lookups = dict()
    tagname = htmlise.make_tagname_decorator(tagname_lookups)

    @tagname("foo")
    def my_func():
        pass

    assert tagname_lookups == {'my_func': "foo"}
    assert callable(my_func)


def test_register_htmliser_func():
    htmliser_funcs = dict()
    htmliser = htmlise.make_htmlise_decorator(htmliser_funcs)

    def make_foo(head, rest):
        pass

    @htmliser(make_foo)
    def my_func():
        pass

    assert htmliser_funcs == {'my_func': make_foo}
    assert callable(my_func)


class TestDoRender(unittest.TestCase):
    """Unittests for do_render"""

    def test_string(self):
        """Test that a string returns itself in a list"""
        datum = """foo"""
        expected = ['foo']
        result = htmlise.do_render(datum, None, None)
        assert expected == result

    def test_list(self):
        """Test that a list is passed to a renderer"""
        tagname_lookups = dict()
        tagname = htmlise.make_tagname_decorator(tagname_lookups)
        htmliser_funcs = dict()
        htmliser = htmlise.make_htmlise_decorator(htmliser_funcs)

        def make_foo(head, rest, *args, **kwargs):
            return repr((head, rest))

        @tagname("footag")
        @htmliser(make_foo)
        def foo():
            pass

        datum = ['foo', "bar"]
        expected = "('foo', ['bar'])"
        result = htmlise.do_render(datum, tagname_lookups, htmliser_funcs)
        assert expected == result


def test_indent_tags():
    "Test that indent_tags indents tags"
    datum = ["a", "b", "c"]
    expected = ["  a", "  b", "  c"]
    result = htmlise.indent_tags(datum)
    assert expected == result


def test_make_block():
    tagname_lookups = dict()
    tagname = htmlise.make_tagname_decorator(tagname_lookups)
    htmliser_funcs = dict()

    @tagname("footag")
    def foo():
        pass

    datum = ['foo', "bar", "baz"]
    expected = [
        "<footag>",
        "  barbaz",
        "</footag>"]
    result = htmlise.make_block(datum[0], datum[1:], tagname_lookups, htmliser_funcs)
    assert expected == result

def test_make_block_with_linebreak():
    tagname_lookups = dict()
    tagname = htmlise.make_tagname_decorator(tagname_lookups)
    htmliser_funcs = dict()

    @tagname("footag")
    def foo():
        pass

    datum = ['foo', "bar", "baz"]
    expected = [
        "<footag>",
        "  barbaz",
        "</footag>",
        ""]
    result = htmlise.make_block_with_linebreak(
        datum[0],
        datum[1:],
        tagname_lookups,
        htmliser_funcs)
    assert expected == result


class TestMakeSpan(unittest.TestCase):
    """Unittests for make_span"""

    def test_simple(self):
        """Test the simplest possible case"""
        tagname_lookups = dict()
        tagname = htmlise.make_tagname_decorator(tagname_lookups)
        htmliser_funcs = dict()

        @tagname("footag")
        def foo():
            pass

        datum = ['foo', "flibble", "flammle"]
        expected = ["<footag>flibbleflammle</footag>"]
        result = htmlise.make_span(datum[0], datum[1:], tagname_lookups, htmliser_funcs)
        assert expected == result

    def test_nested_tagless(self):
        "Test that nested lists work with tagless"
        tagname_lookups = dict()
        tagname = htmlise.make_tagname_decorator(tagname_lookups)
        htmliser_funcs = dict()
        htmliser = htmlise.make_htmlise_decorator(htmliser_funcs)

        @htmliser(htmlise.make_span)
        @tagname(None)
        def foo():
            pass

        datum = [
            'foo',
            ['foo', "flibble", " ", "flammle"],
            " ",
            "flooble ",
            ['foo', "flotsit", " flamagan"]]
        expected = ["flibble flammle flooble flotsit flamagan"]
        result = htmlise.make_span(datum[0], datum[1:], tagname_lookups, htmliser_funcs)
        assert expected == result

    def test_nested_with_tags(self):
        "Test that nested lists work with tags"
        tagname_lookups = dict()
        tagname = htmlise.make_tagname_decorator(tagname_lookups)
        htmliser_funcs = dict()
        htmliser = htmlise.make_htmlise_decorator(htmliser_funcs)

        @htmliser(htmlise.make_span)
        @tagname("tag")
        def foo():
            pass

        datum = [
            'foo',
            ['foo', "flibble", " ", "flammle"],
            " ",
            "flooble ",
            ['foo', "flotsit", " flamagan"]]
        expected = ["<tag><tag>flibble flammle</tag> flooble <tag>flotsit flamagan</tag></tag>"]
        result = htmlise.make_span(datum[0], datum[1:], tagname_lookups, htmliser_funcs)
        assert expected == result


def test_make_span_with_linebreak():
    "Test that make_span_with_linebreak adds a blank line"
    tagname_lookups = dict()
    tagname = htmlise.make_tagname_decorator(tagname_lookups)
    htmliser_funcs = dict()

    @tagname("tag")
    def foo():
        pass

    datum = ['foo', "flibble floozle"]
    expected = ["<tag>flibble floozle</tag>", ""]
    result = htmlise.make_span_with_linebreak(
        datum[0],
        datum[1:],
        tagname_lookups,
        htmliser_funcs)
    assert expected == result


class TestMakeVoidElement(unittest.TestCase):
    """Unittests for make_void_element"""

    def test_simple(self):
        "Test that make_void_element returns a single tag"
        tagname_lookups = dict()
        tagname = htmlise.make_tagname_decorator(tagname_lookups)
        htmliser_funcs = dict()

        @tagname("tag")
        def foo():
            pass

        datum = ['foo', ""]
        expected = ['<tag/>']
        result = htmlise.make_void_element(
            datum[0],
            datum[1:],
            tagname_lookups,
            htmliser_funcs)
        assert expected == result

    def test_ignores_content(self):
        "Test that make_void_element ignores any content"
        tagname_lookups = dict()
        tagname = htmlise.make_tagname_decorator(tagname_lookups)
        htmliser_funcs = dict()

        @tagname("tag")
        def foo():
            pass

        datum = ['foo', "some content"]
        expected = ['<tag/>']
        result = htmlise.make_void_element(
            datum[0],
            datum[1:],
            tagname_lookups,
            htmliser_funcs)
        assert expected == result


def test_make_void_element_with_linebreak():
    "Test that make_void_element_with_linebreak adds an empty line"
    tagname_lookups = dict()
    tagname = htmlise.make_tagname_decorator(tagname_lookups)
    htmliser_funcs = dict()

    @tagname("tag")
    def foo():
        pass

    datum = ['foo', ""]
    expected = ['<tag/>', ""]
    result = htmlise.make_void_element_with_linebreak(
        datum[0],
        datum[1:],
        tagname_lookups,
        htmliser_funcs)
    assert expected == result


def test_make_tagless():
    "Test that make_tagless doesn't put a tag round something"
    tagname_lookups = dict()
    tagname = htmlise.make_tagname_decorator(tagname_lookups)
    htmliser_funcs = dict()
    htmliser = htmlise.make_htmlise_decorator(htmliser_funcs)

    @htmliser(htmlise.make_tagless)
    @tagname("footag")
    def foo():
        pass

    datum = ['foo', "blah"]
    expected = ["blah"]
    result = htmlise.make_tagless(
        datum[0],
        datum[1:],
        tagname_lookups,
        htmliser_funcs)
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
