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
        result = markdown3.parse(data, markdown3.characters)
        assert expected == result

    def test_whitespace(self):
        """Test that characters doesn't match whitespace"""
        data = "two words"
        expected = ['', "two"]
        result = markdown3.parse(data, markdown3.characters)
        assert expected == result


class TestWords(unittest.TestCase):
    """Unittests for words"""
    def test_simple(self):
        """Test that words matches some words"""
        data = "some words"
        expected = ['', "some words"]
        result = markdown3.parse(data, markdown3.words)
        assert expected == result

    def test_many_words(self):
        """Test that words matches multiple words"""
        data = "quite a few words in a row"
        expected = ['', "quite a few words in a row"]
        result = markdown3.parse(data, markdown3.words)
        assert expected == result

    def test_one_word(self):
        """Test that words matches one word"""
        data = "flibble"
        expected = ['', "flibble"]
        result = markdown3.parse(data, markdown3.words)
        assert expected == result

    def test_multiline(self):
        """Test that words doesn't match multiple lines"""
        data = "some words\nover two lines"
        expected = ['', "some words"]
        result = markdown3.parse(data, markdown3.words)
        assert expected == result

    def test_trailing_whitespace(self):
        """Test that words doesn't match trailing whitespace"""
        data = "some words "
        expected = ['', "some words"]
        result = markdown3.parse(data, markdown3.words)
        assert expected == result


class TestEmphasis(unittest.TestCase):
    def test_simple(self):
        data = "*some emphasis*"
        expected = [
            'emphasis',
            "some emphasis"]
        result = markdown3.parse(data, markdown3.emphasis)
        assert expected == result


class TestMultilineWords(unittest.TestCase):
    def test_simple(self):
        data = "some words\nover two lines"
        expected = [
            '',
            "some words",
            " ",
            "over two lines"]
        result = markdown3.parse(data, markdown3.multiline_words)
        assert expected == result


class TestSpan(unittest.TestCase):
    def test_simple(self):
        data = "some words"
        expected = ['', "some words"]
        result = markdown3.parse(data, markdown3.span)
        assert expected == result

    def test_multiline(self):
        "Test that a span only matches one line"
        data = "some words\nover two lines"
        expected = ['', "some words"]
        result = markdown3.parse(data, markdown3.span)

    def test_emphasis(self):
        data = "some words with *emphasis* in them"
        expected = [
            '',
            "some words with",
            " ",
            ['emphasis', "emphasis"],
            " ",
            "in them"]
        result = markdown3.parse(data, markdown3.span)
        assert expected == result


class TestUnorderedBullet(unittest.TestCase):
    def test_simple(self):
        data = "* a bullet"
        expected = [
            'unordered_bullet',
            "a bullet"]
        result = markdown3.parse(data, markdown3.unordered_bullet)
        assert expected == result


class TestUnorderedList(unittest.TestCase):
    """Unittests for unordered list"""

    def test_single_bullet(self):
        """Test that a single bullet matches"""
        data = "* a bullet"
        expected = [
            'unordered_list',
            ['unordered_bullet',
             "a bullet"]]
        result = markdown3.parse(data, markdown3.unordered_list)
        assert expected == result

    def test_multiple_bullets(self):
        """Test that multiple bullets match"""
        data = """
* bullet one
* bullet two
* bullet three""".strip()
        expected = [
            'unordered_list',
            ['unordered_bullet',
             "bullet one"],
            ['unordered_bullet',
             "bullet two"],
            ['unordered_bullet',
             "bullet three"]]
        result = markdown3.parse(data, markdown3.unordered_list)
        assert expected == result

    def test_indented_single_bullet(self):
        data = """  * a bullet"""
        expected = [
            'unordered_list',
            ['unordered_bullet',
             "a bullet"]]
        result = markdown3.parse(data, markdown3.unordered_list)
        assert expected == result

    def test_nested_lists(self):
        """Test that nested lists match"""
        data = """
* bullet one, list one
  * bullet one, list two
        """.strip()
        expected = [
            'unordered_list',
            ['unordered_bullet',
             "bullet one, list one",
             ['unordered_list_nested',
              ['unordered_bullet',
               "bullet one, list two"]]]]
        result = markdown3.parse(data, markdown3.unordered_list)
        assert expected == result


class TestUnorderedListNested(unittest.TestCase):
    """Unittests for unordered_list_nested"""

    def test_unindented(self):
        """Test that unindented doesn't match"""
        with py.test.raises(pg.NoPatternFound):
            data = """
* bullet one
* bullet two""".strip()
            result = markdown3.parse(data, markdown3.unordered_list_nested)

    def test_indented(self):
        data = """    * bullet one\n    * bullet two\n    * bullet three"""
        expected = [
            'unordered_list_nested',
            ['unordered_bullet',
             "bullet one"],
            ['unordered_bullet',
             "bullet two"],
            ['unordered_bullet',
             "bullet three"]]
        result = markdown3.parse(data, markdown3.unordered_list_nested)
        assert expected == result


class TestOrderedBullet(unittest.TestCase):
    """Unittests for ordered_bullet"""

    def test_simple(self):
        """Simplest tests that passes"""
        data = """1. bullet one"""
        expected = [
            'ordered_bullet',
            "bullet one"]
        result = markdown3.parse(data, markdown3.ordered_bullet)
        assert expected == result


class TestOrderedList(unittest.TestCase):
    """Unittests for ordered_list"""

    def test_single_bullet(self):
        """Test that a single bullet matches"""
        data = """1. bullet one"""
        expected = [
            'ordered_list',
            ['ordered_bullet',
             "bullet one"]]
        result = markdown3.parse(data, markdown3.ordered_list)
        assert expected == result

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
        result = markdown3.parse(data, markdown3.ordered_list)
        assert expected == result

    def test_indented_single_bullet(self):
        data = """  1. a bullet"""
        expected = [
            'ordered_list',
            ['ordered_bullet',
             "a bullet"]]
        result = markdown3.parse(data, markdown3.ordered_list)
        assert expected == result

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
        result = markdown3.parse(data, markdown3.ordered_list)
        assert expected == result


class TestLinebreaks(unittest.TestCase):
    """Unittests for linebreaks"""

    def test_single_line(self):
        """Test that linebreaks matches a single blank line """
        data = "\n"
        expected = ([], "")
        result = markdown3.parse(data, markdown3.linebreaks, with_rest=True)
        assert expected == result

    def test_multiple_lines(self):
        """Test that linebreaks matches multiple blank lines"""
        data = "\n\n"
        expected = ([], "")
        result = markdown3.parse(data, markdown3.linebreaks, with_rest=True)
        assert expected == result


class TestHeading1(unittest.TestCase):
    """Unittests for Heading"""

    def test_level_1(self):
        """Test level one heading"""
        data = "# Heading 1 #"
        expected = [
            'heading_1',
            "Heading 1"]
        result = markdown3.parse(data, markdown3.heading_1)
        assert expected == result

    def test_level_1_one_word(self):
        """Test level one heading with only one word"""
        data = "# Heading #"
        expected = [
            'heading_1',
            "Heading"]
        result = markdown3.parse(data, markdown3.heading_1)
        assert expected == result

    def test_level_1_without_end_tag(self):
        """Test level one heading without closing hash"""
        data = "# Heading 1"
        expected = [
            'heading_1',
            "Heading 1"]
        result = markdown3.parse(data, markdown3.heading_1)
        assert expected == result


class TestHeading2(unittest.TestCase):
    """Unittests for Heading"""
    def test_level_2(self):
        """Test level two heading"""
        data = "## Heading 2 ##"
        expected = [
            'heading_2',
            "Heading 2"]
        result = markdown3.parse(data, markdown3.heading_2)
        assert expected == result

    def test_level_2_one_word(self):
        """Test level two heading with only one word"""
        data = "## Heading ##"
        expected = [
            'heading_2',
            "Heading"]
        result = markdown3.parse(data, markdown3.heading_2)
        assert expected == result

    def test_level_2_without_end_tag(self):
        """Test level two heading without closing hash"""
        data = "## Heading 2"
        expected = [
            'heading_2',
            "Heading 2"]
        result = markdown3.parse(data, markdown3.heading_2)
        assert expected == result

def test_paragraph():
    """Test that paragraphs match"""
    data = """A paragraph."""
    expected = [
        'paragraph',
        "A paragraph."]
    result = markdown3.parse(data, markdown3.paragraph)
    assert expected == result
