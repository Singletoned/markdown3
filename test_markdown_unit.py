# -*- coding: utf-8 -*-

import unittest

import py.test

import pegger as pg
import markdown3


class TestCharacters(unittest.TestCase):
    """Unittests for characters"""

    def test_simple(self):
        """Test that characters matches some text"""
        datum = "word"
        expected = ['', "word"]
        result, rest = markdown3.parse(datum, markdown3.characters, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_whitespace(self):
        """Test that characters doesn't match whitespace"""
        datum = "two words"
        expected = ['', "two"]
        result, rest = markdown3.parse(datum, markdown3.characters, with_rest=True)
        assert expected == result
        assert rest == " words"

    def test_quoted_text(self):
        """Test that characters matches quotes"""
        datum = "'word'"
        expected = ['', "'word'"]
        result, rest = markdown3.parse(datum, markdown3.characters, with_rest=True)
        assert expected == result
        assert rest == ""


class TestWords(unittest.TestCase):
    """Unittests for words"""
    def test_simple(self):
        """Test that words matches some words"""
        datum = "some words"
        expected = ['', "some words"]
        result, rest = markdown3.parse(datum, markdown3.words, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_many_words(self):
        """Test that words matches multiple words"""
        datum = "quite a few words in a row"
        expected = ['', "quite a few words in a row"]
        result, rest = markdown3.parse(datum, markdown3.words, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_one_word(self):
        """Test that words matches one word"""
        datum = "flibble"
        expected = ['', "flibble"]
        result, rest = markdown3.parse(datum, markdown3.words, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiline(self):
        """Test that words doesn't match multiple lines"""
        datum = "some words\nover two lines"
        expected = ['', "some words"]
        result, rest = markdown3.parse(datum, markdown3.words, with_rest=True)
        assert expected == result
        assert rest == "\nover two lines"

    def test_trailing_whitespace(self):
        """Test that words doesn't match trailing whitespace"""
        datum = "some words "
        expected = ['', "some words"]
        result, rest = markdown3.parse(datum, markdown3.words, with_rest=True)
        assert expected == result
        assert rest == " "

    def test_quoted_text(self):
        """Test that words matches quotes"""
        datum = """Some words, some of which are "quoted", and some 'not'."""
        expected = ['', """Some words, some of which are "quoted", and some 'not'."""]
        result, rest = markdown3.parse(datum, markdown3.words, with_rest=True)
        assert expected == result
        assert rest == ""


class TestEmphasis(unittest.TestCase):
    """Unittests for emphasis"""
    def test_simple(self):
        datum = "*some emphasis*"
        expected = [
            'emphasis',
            "some emphasis"]
        result, rest = markdown3.parse(datum, markdown3.emphasis, with_rest=True)
        assert expected == result
        assert rest == ""


class TestMultilineWords(unittest.TestCase):
    """Unittests for multiline_words"""
    def test_simple(self):
        datum = "some words\nover two lines"
        expected = [
            '',
            "some words",
            " ",
            "over two lines"]
        result, rest = markdown3.parse(datum, markdown3.multiline_words, with_rest=True)
        assert expected == result
        assert rest == ""


class TestSpan(unittest.TestCase):
    """Unittests for span"""
    def test_simple(self):
        datum = "some words"
        expected = ['', "some words"]
        result, rest = markdown3.parse(datum, markdown3.span, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiline(self):
        "Test that a span only matches one line"
        datum = "some words\nover two lines"
        expected = ['', "some words"]
        result = markdown3.parse(datum, markdown3.span)
        result, rest = markdown3.parse(datum, markdown3.span, with_rest=True)
        assert expected == result
        assert rest == "\nover two lines"

    def test_emphasis(self):
        datum = "some words with *emphasis* in them"
        expected = [
            '',
            "some words with",
            " ",
            ['emphasis', "emphasis"],
            " ",
            "in them"]
        result, rest = markdown3.parse(datum, markdown3.span, with_rest=True)
        assert expected == result
        assert rest == ""


class TestUnorderedBullet(unittest.TestCase):
    """Unittests for unordered_bullet"""
    def test_span(self):
        """Test unordered_bullet with span content"""
        def do_test(bullet):
            datum = "%s a bullet" % bullet
            expected = [
                'unordered_bullet',
                "a bullet"]
            result, rest = markdown3.parse(
                datum,
                markdown3.unordered_bullet(markdown3.span),
                with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_with_tab(self):
        """Test unordered_bullet with tab after the bullet"""
        def do_test(bullet):
            datum = "%s	a bullet" % bullet
            expected = [
                'unordered_bullet',
                "a bullet"]
            result, rest = markdown3.parse(
                datum,
                markdown3.unordered_bullet(markdown3.span),
                with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_paragraph(self):
        """Test unordered_bullet with paragraph content"""
        def do_test(bullet):
            datum = "%s a bullet" % bullet
            expected = [
                'unordered_bullet',
                ['paragraph',
                 "a bullet"]]
            result, rest = markdown3.parse(
                datum,
                markdown3.unordered_bullet(markdown3.paragraph),
                with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_nested_list_in_bullet(self):
        """Test that a bullet can match a nested list"""
        datum = """
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
            datum,
            markdown3.unordered_bullet(markdown3.span),
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multi_paragraph_bullet(self):
        def do_test(datum):
            expected = [
                'unordered_bullet',
                ['paragraph',
                 "bullet one, paragraph one"],
                ['paragraph',
                 "bullet one, paragraph two"]]
            result, rest = markdown3.parse(
                datum,
                markdown3.unordered_bullet(markdown3._multiple_paragraphs),
                with_rest=True)
            assert expected == result
            assert rest == ""

        data = [
"""
* bullet one, paragraph one

  bullet one, paragraph two""".strip(),
"""
*	bullet one, paragraph one

	bullet one, paragraph two""".strip()]

        for datum in data:
            do_test(datum)


class TestUnorderedList(unittest.TestCase):
    """Unittests for unordered list"""

    def test_single_bullet(self):
        """Test that a single bullet matches"""
        def do_test(bullet):
            datum = "%s a bullet" % bullet
            expected = [
                'unordered_list',
                ['unordered_bullet',
                 "a bullet"]]
            result, rest = markdown3.parse(datum, markdown3.unordered_list, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_multiple_bullets(self):
        """Test that multiple bullets match"""
        def do_test(bullet):
            datum = """
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
            result, rest = markdown3.parse(datum, markdown3.unordered_list, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_multiple_bullets_with_tabs(self):
        """Test that multiple bullets match"""
        def do_test(bullet):
            datum = """
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
                datum,
                markdown3.unordered_list,
                with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_indented_single_bullet(self):
        def do_test(bullet):
            datum = """  %s a bullet""" % bullet
            expected = [
                'unordered_list',
                ['unordered_bullet',
                 "a bullet"]]
            result, rest = markdown3.parse(datum, markdown3.unordered_list, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_nested_lists(self):
        """Test that nested lists match"""
        def do_test(bullet):
            datum = """
    %(bullet)s bullet one, list one
      %(bullet)s bullet one, list two
            """.strip() % dict(bullet=bullet)
            expected = [
                'unordered_list',
                ['unordered_bullet',
                 "bullet one, list one",
                 ['unordered_list',
                  ['unordered_bullet',
                   "bullet one, list two"]]]]
            result, rest = markdown3.parse(datum, markdown3.unordered_list, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_with_paragraphs(self):
        """Test that padding between lines creates paragraphs"""
        def do_test(bullet):
            datum = """
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

            result, rest = markdown3.parse(datum, markdown3.unordered_list, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_multi_paragraph_list(self):
        def do_test(datum):
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
                datum,
                markdown3.unordered_list,
                with_rest=True)
            assert expected == result
            assert rest == ""

        data = [
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
        for datum in data:
            do_test(datum)


class TestUnorderedListNested(unittest.TestCase):
    """Unittests for unordered_list_nested"""

    def test_unindented(self):
        """Test that unindented doesn't match"""
        def do_test(bullet):
            with py.test.raises(pg.NoPatternFound):
                datum = """
%(bullet)s bullet one
%(bullet)s bullet two""".strip() % dict(bullet=bullet)
                result = markdown3.parse(datum, markdown3.unordered_list_nested)

        for bullet in ["*", "+", "-"]:
            do_test(bullet)

    def test_indented(self):
        def do_test(bullet):
            datum = """    %(bullet)s bullet one\n    %(bullet)s bullet two\n    %(bullet)s bullet three""" % dict(bullet=bullet)
            expected = [
                'unordered_list_nested',
                ['unordered_bullet',
                 "bullet one"],
                ['unordered_bullet',
                 "bullet two"],
                ['unordered_bullet',
                 "bullet three"]]
            result, rest = markdown3.parse(datum, markdown3.unordered_list_nested, with_rest=True)
            assert expected == result
            assert rest == ""

        for bullet in ["*", "+", "-"]:
            do_test(bullet)


class TestOrderedBullet(unittest.TestCase):
    """Unittests for ordered_bullet"""

    def test_span(self):
        """Test ordered_bullet with span content"""
        def do_test(indent):
            datum = """1.%sbullet one""" % indent
            expected = [
                'ordered_bullet',
                "bullet one"]
            result, rest = markdown3.parse(
                datum,
                markdown3.ordered_bullet(markdown3.span),
                with_rest=True)
            assert expected == result
            assert rest == ""

        for indent in [" ", "\t"]:
            do_test(indent)

    def test_paragraph(self):
        """Test ordered_bullet with paragraph content"""
        def do_test(indent):
            datum = """1.%sbullet one""" % indent
            expected = [
                'ordered_bullet',
                ['paragraph',
                 "bullet one"]]
            result, rest = markdown3.parse(
                datum,
                markdown3.ordered_bullet(markdown3.paragraph),
                with_rest=True)
            assert expected == result
            assert rest == ""

        for indent in [" ", "\t"]:
            do_test(indent)

    def test_nested_list_in_bullet(self):
        """Test that a bullet can match a nested list"""
        datum = """
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
            datum,
            markdown3.ordered_bullet(markdown3.span),
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multi_paragraph_bullet(self):
        def do_test(datum):
            expected = [
                'ordered_bullet',
                ['paragraph',
                 "bullet one, paragraph one"],
                ['paragraph',
                 "bullet one, paragraph two"]]
            result, rest = markdown3.parse(
                datum,
                markdown3.ordered_bullet(markdown3._multiple_paragraphs),
                with_rest=True)
            assert expected == result
            assert rest == ""

        data = [
"""
1. bullet one, paragraph one

   bullet one, paragraph two""".strip(),
"""
1.	bullet one, paragraph one

	bullet one, paragraph two""".strip()]
        for datum in data:
            do_test(datum)


class TestOrderedList(unittest.TestCase):
    """Unittests for ordered_list"""

    def test_single_bullet(self):
        """Test that a single bullet matches"""
        datum = """1. bullet one"""
        expected = [
            'ordered_list',
            ['ordered_bullet',
             "bullet one"]]
        result, rest = markdown3.parse(datum, markdown3.ordered_list, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiple_bullets(self):
        """Test that multiple bullets match"""
        datum = """
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
        result, rest = markdown3.parse(datum, markdown3.ordered_list, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_indented_single_bullet(self):
        datum = """  1. a bullet"""
        expected = [
            'ordered_list',
            ['ordered_bullet',
             "a bullet"]]
        result, rest = markdown3.parse(datum, markdown3.ordered_list, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_nested_lists(self):
        """Test that nested lists match"""
        datum = """
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
        result, rest = markdown3.parse(datum, markdown3.ordered_list, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_with_paragraphs(self):
        """Test that padding between lines creates paragraphs"""
        datum = """
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

        result, rest = markdown3.parse(datum, markdown3.ordered_list, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multi_paragraph_list(self):
        def do_test(datum):
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
                datum,
                markdown3.ordered_list,
                with_rest=True)
            assert expected == result
            assert rest == ""

        data = ["""
1. bullet one, paragraph one

   bullet one, paragraph two

2. bullet two, paragraph one

3. bullet three, paragraph one""".strip(),
"""
1.	bullet one, paragraph one

	bullet one, paragraph two

2.	bullet two, paragraph one

3.	bullet three, paragraph one""".strip()]
        for datum in data:
            do_test(datum)


class TestLinebreaks(unittest.TestCase):
    """Unittests for linebreaks"""

    def test_single_line(self):
        """Test that linebreaks matches a single blank line """
        datum = "\n"
        expected = []
        result, rest = markdown3.parse(datum, markdown3.linebreaks, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiple_lines(self):
        """Test that linebreaks matches multiple blank lines"""
        datum = "\n\n"
        expected = []
        result, rest = markdown3.parse(datum, markdown3.linebreaks, with_rest=True)
        assert expected == result
        assert rest == ""


class TestHeading1(unittest.TestCase):
    """Unittests for Heading"""

    def test_level_1(self):
        """Test level one heading"""
        datum = "# Heading 1 #"
        expected = [
            'heading_1',
            "Heading 1"]
        result, rest = markdown3.parse(datum, markdown3.heading_1, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_level_1_one_word(self):
        """Test level one heading with only one word"""
        datum = "# Heading #"
        expected = [
            'heading_1',
            "Heading"]
        result, rest = markdown3.parse(datum, markdown3.heading_1, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_level_1_without_end_tag(self):
        """Test level one heading without closing hash"""
        datum = "# Heading 1"
        expected = [
            'heading_1',
            "Heading 1"]
        result, rest = markdown3.parse(datum, markdown3.heading_1, with_rest=True)
        assert expected == result
        assert rest == ""


class TestHeading2(unittest.TestCase):
    """Unittests for Heading"""
    def test_level_2(self):
        """Test level two heading"""
        datum = "## Heading 2 ##"
        expected = [
            'heading_2',
            "Heading 2"]
        result, rest = markdown3.parse(datum, markdown3.heading_2, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_level_2_one_word(self):
        """Test level two heading with only one word"""
        datum = "## Heading ##"
        expected = [
            'heading_2',
            "Heading"]
        result, rest = markdown3.parse(datum, markdown3.heading_2, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_level_2_without_end_tag(self):
        """Test level two heading without closing hash"""
        datum = "## Heading 2"
        expected = [
            'heading_2',
            "Heading 2"]
        result, rest = markdown3.parse(datum, markdown3.heading_2, with_rest=True)
        assert expected == result
        assert rest == ""


class TestParagraph(unittest.TestCase):
    """Unittests for paragraph"""

    def test_simple(self):
        """Simplest possible test"""
        datum = """A paragraph."""
        expected = [
            'paragraph',
            "A paragraph."]
        result, rest = markdown3.parse(datum, markdown3.paragraph, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_with_emphasis(self):
        """Test that paragraph matches emphasis"""
        datum = """A paragraph with *some emphasis* in it"""
        expected = [
            'paragraph',
            "A paragraph with",
            " ",
            ['emphasis',
             "some emphasis"],
            " ",
            "in it"]
        result, rest = markdown3.parse(datum, markdown3.paragraph, with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiline(self):
        """Test that a paragraph can contain single linebreaks"""
        datum = """A paragraph that spans\nmultiple lines."""
        expected = [
            'paragraph',
            "A paragraph that spans",
            " ",
            "multiple lines."]
        result, rest = markdown3.parse(
            datum,
            markdown3.paragraph,
            with_rest=True)
        assert expected == result


class TestMultipleParagraphs(unittest.TestCase):
    """Unittests for _multiple_paragraphs"""

    def test_simple(self):
        """Simplest test"""
        datum = """Paragraph 1"""
        expected = [
            '_multiple_paragraphs',
            ['paragraph',
             "Paragraph 1"]]
        result, rest = markdown3.parse(
            datum,
            markdown3._multiple_paragraphs,
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_multiple_paragraphs(self):
        """Test that it matches multiple paragraphs"""
        datum = """Paragraph 1\n\nParagraph 2"""
        expected = [
            '_multiple_paragraphs',
            ['paragraph',
             "Paragraph 1"],
            ['paragraph',
             "Paragraph 2"]]
        result, rest = markdown3.parse(
            datum,
            markdown3._multiple_paragraphs,
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_single_paragraph_with_rest(self):
        """Test that matching a single paragraph returns any trailing linebreaks"""
        datum = """Paragraph 1\n\n"""
        expected = [
            '_multiple_paragraphs',
            ['paragraph',
             "Paragraph 1"]]
        result, rest = markdown3.parse(
            datum,
            markdown3._multiple_paragraphs,
            with_rest=True)
        assert expected == result
        assert rest == "\n\n"

    def test_multiline(self):
        """Test that paragraphs can contain single linebreaks"""
        datum = """
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
            datum,
            markdown3._multiple_paragraphs,
            with_rest=True)
        assert expected == result


class TestHorizontalRule(unittest.TestCase):
    """Unittests for horizontal rule"""

    def test_simple(self):
        """Simplest test that can pass"""
        def do_test(datum):
            expected = [
                'horizontal_rule',
                ""]
            result, rest = markdown3.parse(
                datum,
                markdown3.horizontal_rule,
                with_rest=True)
            assert expected == result
            assert rest == ""

        data = [
            "***",
            "* * *",
            "---",
            "- - -",
            "___",
            "_ _ _"]

        for datum in data:
            for suffix in [
                "",
                "**",
                "--",
                "__",
                "foo"]:
                do_test(datum+suffix)


class TestBlankLine(unittest.TestCase):
    """Unittests for _blankline"""

    def test_matches(self):
        """Test that blank line matches newline+whitespace+newline"""
        def do_test(datum):
            expected = []
            result, rest = markdown3.parse(
                datum,
                markdown3._blank_line,
                with_rest=True)
            assert expected == result
            assert rest == ""

        data = [
            "\n  \n",
            "\n \n",
            "\n\n",
            "\n	\n",
            "\n		\n"]

        for datum in data:
            do_test(datum)

    def test_failures(self):
        """Test that _blank_line doesn't match various things"""
        def do_test(datum):
            with py.test.raises(pg.NoPatternFound):
                result, rest = markdown3.parse(
                    datum,
                    markdown3._blank_line,
                    with_rest=True)
        data = [
            "\n",
            "\na\n"]

        for datum in data:
            do_test(datum)


class TestLink(unittest.TestCase):
    """Unittests for link"""

    def test_link_url(self):
        """Test that the link part matches"""
        datum = "http://foo.com"
        expected = ['link_url', "http://foo.com"]
        result, rest = markdown3.parse(
            datum,
            markdown3.link_url,
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_link_url_with_title(self):
        """Test that the link part matches, but not past a space"""
        datum = "http://foo.com foo"
        expected = ['link_url', "http://foo.com"]
        result, rest = markdown3.parse(
            datum,
            markdown3.link_url,
            with_rest=True)
        assert expected == result
        assert rest == " foo"

    def test_link_title(self):
        """Test that the title part matches"""
        datum = ''' "Foo"'''
        expected = ['link_title', "Foo"]
        result, rest = markdown3.parse(
            datum,
            markdown3.link_title,
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_link_text(self):
        """Test that the text part matches"""
        datum = "[foo]"
        expected = ['link_text', "foo"]
        result, rest = markdown3.parse(
            datum,
            markdown3.link_text,
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_link_without_title(self):
        """Test that a whole link matches by itself"""
        datum = "[a link to Google](http://www.google.com)"
        expected = [
            'link',
            ['link_text',
             "a link to Google"],
            ['link_url',
             "http://www.google.com"]]
        result, rest = markdown3.parse(
            datum,
            markdown3.link,
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_link_with_title(self):
        """Test that the url part can have a title"""
        datum = '[a link to Google](http://www.google.com "Google")'
        expected = [
            'link',
            ['link_text',
             "a link to Google"],
            ['link_url',
             "http://www.google.com"],
            ['link_title',
             "Google"]]
        result, rest = markdown3.parse(
            datum,
            markdown3.link,
            with_rest=True)
        assert expected == result
        assert rest == ""

    def test_paragraph_with_link_with_title(self):
        """Test that a link matches as part of a paragraph"""
        datum = """some text with [a link to Google](http://www.google.com "Google!") in it"""
        expected = [
            'paragraph',
            "some text with",
            " ",
            ['link',
             ['link_text',
              "a link to Google"],
             ['link_url',
              "http://www.google.com"],
             ['link_title',
              "Google!"]],
            " ",
            "in it"]
        result, rest = markdown3.parse(
            datum,
            markdown3.paragraph,
            with_rest=True)
        assert expected == result
        assert rest == ""
