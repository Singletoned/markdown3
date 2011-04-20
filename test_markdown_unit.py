# -*- coding: utf-8 -*-

import unittest

import py.test

import pegger as pg
import markdown3


class TestCharacters(unittest.TestCase):
    """Unittests for characters"""

    def test_simple(self):
        """Test that characters matches some text"""
        data = "word"
        expected = ['', "word"]
        result, rest = markdown3.parse(data, markdown3.characters, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_whitespace(self):
        """Test that characters doesn't match whitespace"""
        data = "two words"
        expected = ['', "two"]
        result, rest = markdown3.parse(data, markdown3.characters, with_rest=True)
        assert expected == result
        assert rest == " words"


class TestWords(unittest.TestCase):
    """Unittests for words"""
    def test_simple(self):
        """Test that words matches some words"""
        data = "some words"
        expected = ['', "some words"]
        result, rest = markdown3.parse(data, markdown3.words, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_many_words(self):
        """Test that words matches multiple words"""
        data = "quite a few words in a row"
        expected = ['', "quite a few words in a row"]
        result, rest = markdown3.parse(data, markdown3.words, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_one_word(self):
        """Test that words matches one word"""
        data = "flibble"
        expected = ['', "flibble"]
        result, rest = markdown3.parse(data, markdown3.words, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiline(self):
        """Test that words doesn't match multiple lines"""
        data = "some words\nover two lines"
        expected = ['', "some words"]
        result, rest = markdown3.parse(data, markdown3.words, with_rest=True)
        assert expected == result
        assert rest == "\nover two lines"

    def test_trailing_whitespace(self):
        """Test that words doesn't match trailing whitespace"""
        data = "some words "
        expected = ['', "some words"]
        result, rest = markdown3.parse(data, markdown3.words, with_rest=True)
        assert expected == result
        assert rest == " "


class TestEmphasis(unittest.TestCase):
    def test_simple(self):
        data = "*some emphasis*"
        expected = [
            'emphasis',
            "some emphasis"]
        result, rest = markdown3.parse(data, markdown3.emphasis, with_rest=True)
        assert expected == result
        assert rest == ""


class TestMultilineWords(unittest.TestCase):
    def test_simple(self):
        data = "some words\nover two lines"
        expected = [
            '',
            "some words",
            " ",
            "over two lines"]
        result, rest = markdown3.parse(data, markdown3.multiline_words, with_rest=True)
        assert expected == result
        assert rest == ""


class TestSpan(unittest.TestCase):
    def test_simple(self):
        data = "some words"
        expected = ['', "some words"]
        result, rest = markdown3.parse(data, markdown3.span, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiline(self):
        "Test that a span only matches one line"
        data = "some words\nover two lines"
        expected = ['', "some words"]
        result = markdown3.parse(data, markdown3.span)
        result, rest = markdown3.parse(data, markdown3.span, with_rest=True)
        assert expected == result
        assert rest == "\nover two lines"

    def test_emphasis(self):
        data = "some words with *emphasis* in them"
        expected = [
            '',
            "some words with",
            " ",
            ['emphasis', "emphasis"],
            " ",
            "in them"]
        result, rest = markdown3.parse(data, markdown3.span, with_rest=True)
        assert expected == result
        assert rest == ""


class TestUnorderedBullet(unittest.TestCase):
    def test_span(self):
        """Test unordered_bullet with span content"""
        def do_test(bullet):
            data = "%s a bullet" % bullet
            expected = [
                'unordered_bullet',
                "a bullet"]
            result, rest = markdown3.parse(
                data,
                markdown3.unordered_bullet(markdown3.span),
                with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_with_tab(self):
        """Test unordered_bullet with tab after the bullet"""
        def do_test(bullet):
            data = "%s	a bullet" % bullet
            expected = [
                'unordered_bullet',
                "a bullet"]
            result, rest = markdown3.parse(
                data,
                markdown3.unordered_bullet(markdown3.span),
                with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_paragraph(self):
        """Test unordered_bullet with paragraph content"""
        def do_test(bullet):
            data = "%s a bullet" % bullet
            expected = [
                'unordered_bullet',
                ['paragraph',
                 "a bullet"]]
            result, rest = markdown3.parse(
                data,
                markdown3.unordered_bullet(markdown3.paragraph),
                with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_nested_list_in_bullet(self):
        """Test that a bullet can match a nested list"""
        data = """
* list 1, bullet 1
   * list 2, bullet 1
   * list 2, bullet 2""".strip()
        expected = [
            'unordered_bullet',
            "list 1, bullet 1",
            ['unordered_list_nested',
             ['unordered_bullet',
              "list 2, bullet 1"],
             ['unordered_bullet',
              "list 2, bullet 2"]]]

        result, rest = markdown3.parse(
            data,
            markdown3.unordered_bullet(markdown3.span),
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multi_paragraph_bullet(self):
        def do_test(data):
            expected = [
                'unordered_bullet',
                ['paragraph',
                 "bullet one, paragraph one"],
                ['paragraph',
                 "bullet one, paragraph two"]]
            result, rest = markdown3.parse(
                data,
                markdown3.unordered_bullet(markdown3._multiple_paragraphs),
                with_rest=True)
            assert expected == result
            assert rest == ""

        datas = [
"""
* bullet one, paragraph one

  bullet one, paragraph two""".strip(),
"""
*	bullet one, paragraph one

	bullet one, paragraph two""".strip()]

        for data in datas:
            do_test(data)


class TestUnorderedList(unittest.TestCase):
    """Unittests for unordered list"""

    def test_single_bullet(self):
        """Test that a single bullet matches"""
        def do_test(bullet):
            data = "%s a bullet" % bullet
            expected = [
                'unordered_list',
                ['unordered_bullet',
                 "a bullet"]]
            result, rest = markdown3.parse(data, markdown3.unordered_list, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_multiple_bullets(self):
        """Test that multiple bullets match"""
        def do_test(bullet):
            data = """
%(bullet)s bullet one
%(bullet)s bullet two
%(bullet)s bullet three""".strip() % dict(bullet=bullet)
            expected = [
                'unordered_list',
                ['unordered_bullet',
                 "bullet one"],
                ['unordered_bullet',
                 "bullet two"],
                ['unordered_bullet',
                 "bullet three"]]
            result, rest = markdown3.parse(data, markdown3.unordered_list, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_multiple_bullets_with_tabs(self):
        """Test that multiple bullets match"""
        def do_test(bullet):
            data = """
%(bullet)s	bullet one
%(bullet)s	bullet two
%(bullet)s	bullet three""".strip() % dict(bullet=bullet)
            expected = [
                'unordered_list',
                ['unordered_bullet',
                 "bullet one"],
                ['unordered_bullet',
                 "bullet two"],
                ['unordered_bullet',
                 "bullet three"]]
            result, rest = markdown3.parse(
                data,
                markdown3.unordered_list,
                with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_indented_single_bullet(self):
        def do_test(bullet):
            data = """  %s a bullet""" % bullet
            expected = [
                'unordered_list',
                ['unordered_bullet',
                 "a bullet"]]
            result, rest = markdown3.parse(data, markdown3.unordered_list, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_nested_lists(self):
        """Test that nested lists match"""
        def do_test(bullet):
            data = """
    %(bullet)s bullet one, list one
      %(bullet)s bullet one, list two
            """.strip() % dict(bullet=bullet)
            expected = [
                'unordered_list',
                ['unordered_bullet',
                 "bullet one, list one",
                 ['unordered_list_nested',
                  ['unordered_bullet',
                   "bullet one, list two"]]]]
            result, rest = markdown3.parse(data, markdown3.unordered_list, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_with_paragraphs(self):
        """Test that padding between lines creates paragraphs"""
        def do_test(bullet):
            data = """
%(bullet)s item 1

%(bullet)s item 2

%(bullet)s item 3""".strip() % dict(bullet=bullet)
            expected = [
                'unordered_list',
                ['unordered_bullet',
                 ['paragraph', "item 1"]],
                ['unordered_bullet',
                 ['paragraph', "item 2"]],
                ['unordered_bullet',
                 ['paragraph', "item 3"]]]

            result, rest = markdown3.parse(data, markdown3.unordered_list, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_multi_paragraph_list(self):
        def do_test(data):
            expected = [
                'unordered_list',
                ['unordered_bullet',
                 ['paragraph',
                  "bullet one, paragraph one"],
                 ['paragraph',
                  "bullet one, paragraph two"]],
                ['unordered_bullet',
                 ['paragraph',
                  "bullet two, paragraph one"]],
                ['unordered_bullet',
                 ['paragraph',
                  "bullet three, paragraph one"]]]
            result, rest = markdown3.parse(
                data,
                markdown3.unordered_list,
                with_rest=True)
            assert expected == result
            assert rest == ""

        datas = [
"""
* bullet one, paragraph one

  bullet one, paragraph two

* bullet two, paragraph one

* bullet three, paragraph one""".strip(),
"""
*	bullet one, paragraph one

	bullet one, paragraph two

*	bullet two, paragraph one

*	bullet three, paragraph one""".strip()]
        for data in datas:
            do_test(data)


class TestUnorderedListNested(unittest.TestCase):
    """Unittests for unordered_list_nested"""

    def test_unindented(self):
        """Test that unindented doesn't match"""
        def do_test(bullet):
            with py.test.raises(pg.NoPatternFound):
                data = """
%(bullet)s bullet one
%(bullet)s bullet two""".strip() % dict(bullet=bullet)
                result = markdown3.parse(data, markdown3.unordered_list_nested)

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_indented(self):
        def do_test(bullet):
            data = """    %(bullet)s bullet one\n    %(bullet)s bullet two\n    %(bullet)s bullet three""" % dict(bullet=bullet)
            expected = [
                'unordered_list_nested',
                ['unordered_bullet',
                 "bullet one"],
                ['unordered_bullet',
                 "bullet two"],
                ['unordered_bullet',
                 "bullet three"]]
            result, rest = markdown3.parse(data, markdown3.unordered_list_nested, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)


class TestOrderedBullet(unittest.TestCase):
    """Unittests for ordered_bullet"""

    def test_span(self):
        """Test ordered_bullet with span content"""
        def do_test(indent):
            data = """1.%sbullet one""" % indent
            expected = [
                'ordered_bullet',
                "bullet one"]
            result, rest = markdown3.parse(
                data,
                markdown3.ordered_bullet(markdown3.span),
                with_rest=True)
            assert expected == result
            assert rest == ""

        for indent in [" ", "\t"]:
            do_test(indent)

    def test_paragraph(self):
        """Test ordered_bullet with paragraph content"""
        def do_test(indent):
            data = """1.%sbullet one""" % indent
            expected = [
                'ordered_bullet',
                ['paragraph',
                 "bullet one"]]
            result, rest = markdown3.parse(
                data,
                markdown3.ordered_bullet(markdown3.paragraph),
                with_rest=True)
            assert expected == result
            assert rest == ""

        for indent in [" ", "\t"]:
            do_test(indent)

    def test_nested_list_in_bullet(self):
        """Test that a bullet can match a nested list"""
        data = """
1. list 1, bullet 1
   2. list 2, bullet 1
   3. list 2, bullet 2""".strip()
        expected = [
            'ordered_bullet',
            "list 1, bullet 1",
            ['ordered_list_nested',
             ['ordered_bullet',
              "list 2, bullet 1"],
             ['ordered_bullet',
              "list 2, bullet 2"]]]

        result, rest = markdown3.parse(
            data,
            markdown3.ordered_bullet(markdown3.span),
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multi_paragraph_bullet(self):
        def do_test(data):
            expected = [
                'ordered_bullet',
                ['paragraph',
                 "bullet one, paragraph one"],
                ['paragraph',
                 "bullet one, paragraph two"]]
            result, rest = markdown3.parse(
                data,
                markdown3.ordered_bullet(markdown3._multiple_paragraphs),
                with_rest=True)
            assert expected == result
            assert rest == ""

        datas = [
"""
1. bullet one, paragraph one

   bullet one, paragraph two""".strip(),
"""
1.	bullet one, paragraph one

	bullet one, paragraph two""".strip()]
        for data in datas:
            do_test(data)


class TestOrderedList(unittest.TestCase):
    """Unittests for ordered_list"""

    def test_single_bullet(self):
        """Test that a single bullet matches"""
        data = """1. bullet one"""
        expected = [
            'ordered_list',
            ['ordered_bullet',
             "bullet one"]]
        result, rest = markdown3.parse(data, markdown3.ordered_list, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiple_bullets(self):
        """Test that multiple bullets match"""
        data = """
1. bullet one
2. bullet two
3. bullet three""".strip()
        expected = [
            'ordered_list',
            ['ordered_bullet',
             "bullet one"],
            ['ordered_bullet',
             "bullet two"],
            ['ordered_bullet',
             "bullet three"]]
        result, rest = markdown3.parse(data, markdown3.ordered_list, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_indented_single_bullet(self):
        data = """  1. a bullet"""
        expected = [
            'ordered_list',
            ['ordered_bullet',
             "a bullet"]]
        result, rest = markdown3.parse(data, markdown3.ordered_list, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_nested_lists(self):
        """Test that nested lists match"""
        data = """
1. bullet one, list one
  1. bullet one, list two
        """.strip()
        expected = [
            'ordered_list',
            ['ordered_bullet',
             "bullet one, list one",
             ['ordered_list_nested',
              ['ordered_bullet',
               "bullet one, list two"]]]]
        result, rest = markdown3.parse(data, markdown3.ordered_list, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_with_paragraphs(self):
        """Test that padding between lines creates paragraphs"""
        data = """
1. item 1

2. item 2

3. item 3""".strip()
        expected = [
            'ordered_list',
            ['ordered_bullet',
             ['paragraph', "item 1"]],
            ['ordered_bullet',
             ['paragraph', "item 2"]],
            ['ordered_bullet',
             ['paragraph', "item 3"]]]

        result, rest = markdown3.parse(data, markdown3.ordered_list, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multi_paragraph_list(self):
        def do_test(data):
            expected = [
                'ordered_list',
                ['ordered_bullet',
                 ['paragraph',
                  "bullet one, paragraph one"],
                 ['paragraph',
                  "bullet one, paragraph two"]],
                ['ordered_bullet',
                 ['paragraph',
                  "bullet two, paragraph one"]],
                ['ordered_bullet',
                 ['paragraph',
                  "bullet three, paragraph one"]]]
            result, rest = markdown3.parse(
                data,
                markdown3.ordered_list,
                with_rest=True)
            assert expected == result
            assert rest == ""

        datas = ["""
1. bullet one, paragraph one

   bullet one, paragraph two

2. bullet two, paragraph one

3. bullet three, paragraph one""".strip(),
"""
1.	bullet one, paragraph one

	bullet one, paragraph two

2.	bullet two, paragraph one

3.	bullet three, paragraph one""".strip()]
        for data in datas:
            do_test(data)


class TestLinebreaks(unittest.TestCase):
    """Unittests for linebreaks"""

    def test_single_line(self):
        """Test that linebreaks matches a single blank line """
        data = "\n"
        expected = []
        result, rest = markdown3.parse(data, markdown3.linebreaks, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiple_lines(self):
        """Test that linebreaks matches multiple blank lines"""
        data = "\n\n"
        expected = []
        result, rest = markdown3.parse(data, markdown3.linebreaks, with_rest=True)
        assert expected == result
        assert rest == ""


class TestHeading1(unittest.TestCase):
    """Unittests for Heading"""

    def test_level_1(self):
        """Test level one heading"""
        data = "# Heading 1 #"
        expected = [
            'heading_1',
            "Heading 1"]
        result, rest = markdown3.parse(data, markdown3.heading_1, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_level_1_one_word(self):
        """Test level one heading with only one word"""
        data = "# Heading #"
        expected = [
            'heading_1',
            "Heading"]
        result, rest = markdown3.parse(data, markdown3.heading_1, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_level_1_without_end_tag(self):
        """Test level one heading without closing hash"""
        data = "# Heading 1"
        expected = [
            'heading_1',
            "Heading 1"]
        result, rest = markdown3.parse(data, markdown3.heading_1, with_rest=True)
        assert expected == result
        assert rest == ""


class TestHeading2(unittest.TestCase):
    """Unittests for Heading"""
    def test_level_2(self):
        """Test level two heading"""
        data = "## Heading 2 ##"
        expected = [
            'heading_2',
            "Heading 2"]
        result, rest = markdown3.parse(data, markdown3.heading_2, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_level_2_one_word(self):
        """Test level two heading with only one word"""
        data = "## Heading ##"
        expected = [
            'heading_2',
            "Heading"]
        result, rest = markdown3.parse(data, markdown3.heading_2, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_level_2_without_end_tag(self):
        """Test level two heading without closing hash"""
        data = "## Heading 2"
        expected = [
            'heading_2',
            "Heading 2"]
        result, rest = markdown3.parse(data, markdown3.heading_2, with_rest=True)
        assert expected == result
        assert rest == ""


class TestParagraph(unittest.TestCase):
    """Unittests for paragraph"""

    def test_simple(self):
        """Simplest possible test"""
        data = """A paragraph."""
        expected = [
            'paragraph',
            "A paragraph."]
        result, rest = markdown3.parse(data, markdown3.paragraph, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_with_emphasis(self):
        """Test that paragraph matches emphasis"""
        data = """A paragraph with *some emphasis* in it"""
        expected = [
            'paragraph',
            "A paragraph with",
            " ",
            ['emphasis',
             "some emphasis"],
            " ",
            "in it"]
        result, rest = markdown3.parse(data, markdown3.paragraph, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiline(self):
        """Test that a paragraph can contain single linebreaks"""
        data = """A paragraph that spans\nmultiple lines."""
        expected = [
            'paragraph',
            "A paragraph that spans",
            " ",
            "multiple lines."]
        result, rest = markdown3.parse(
            data,
            markdown3.paragraph,
            with_rest=True)
        assert expected == result


class TestMultipleParagraphs(unittest.TestCase):
    """Unittests for _multiple_paragraphs"""

    def test_simple(self):
        """Simplest test"""
        data = """Paragraph 1"""
        expected = [
            '_multiple_paragraphs',
            ['paragraph',
             "Paragraph 1"]]
        result, rest = markdown3.parse(
            data,
            markdown3._multiple_paragraphs,
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiple_paragraphs(self):
        """Test that it matches multiple paragraphs"""
        data = """Paragraph 1\n\nParagraph 2"""
        expected = [
            '_multiple_paragraphs',
            ['paragraph',
             "Paragraph 1"],
            ['paragraph',
             "Paragraph 2"]]
        result, rest = markdown3.parse(
            data,
            markdown3._multiple_paragraphs,
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_single_paragraph_with_rest(self):
        """Test that matching a single paragraph returns any trailing linebreaks"""
        data = """Paragraph 1\n\n"""
        expected = [
            '_multiple_paragraphs',
            ['paragraph',
             "Paragraph 1"]]
        result, rest = markdown3.parse(
            data,
            markdown3._multiple_paragraphs,
            with_rest=True)
        assert expected == result
        assert rest == "\n\n"

    def test_multiline(self):
        """Test that paragraphs can contain single linebreaks"""
        data = """
A paragraph that spans
multiple lines.

Another paragraph
over multiple lines.""".strip()
        expected = [
            '_multiple_paragraphs',
            ['paragraph',
             "A paragraph that spans",
             " ",
             "multiple lines."],
            ['paragraph',
             "Another paragraph",
             " ",
             "over multiple lines."]]
        result, rest = markdown3.parse(
            data,
            markdown3._multiple_paragraphs,
            with_rest=True)
        assert expected == result


class TestHorizontalRule(unittest.TestCase):
    """Unittests for horizontal rule"""

    def test_simple(self):
        """Simplest test that can pass"""
        def do_test(data):
            expected = [
                'horizontal_rule',
                ""]
            result, rest = markdown3.parse(
                data,
                markdown3.horizontal_rule,
                with_rest=True)
            assert expected == result
            assert rest == ""

        for data in [
            "***",
            "* * *",
            "---",
            "- - -",
            "___",
            "_ _ _"]:
            for suffix in [
                "",
                "**",
                "--",
                "__",
                "foo"]:
                do_test(data+suffix)
