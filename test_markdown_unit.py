# -*- coding: utf-8 -*-

import unittest

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
* bullet two""".strip()
        expected = [
            'unordered_list',
            ['unordered_bullet',
             "bullet one"],
            ['unordered_bullet',
             "bullet two"]]
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
