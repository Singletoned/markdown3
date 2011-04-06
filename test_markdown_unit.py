# -*- coding: utf-8 -*-

import unittest

import py.test

import pegger as pg
import markdown3

class TestWords(unittest.TestCase):
    def test_simple(self):
        data = "some words"
        expected = ['', "some words"]
        result = markdown3.parse(data, markdown3.words)
        assert expected == result

    def test_multiline(self):
        data = "some words\nover two lines"
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
            "some words with ",
            ['emphasis', "emphasis"],
            " in them"]
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
