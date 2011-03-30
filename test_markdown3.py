# -*- coding: utf-8 -*-

import unittest

import markdown3

def test_body():
    data = "Hello World"
    expected = [
        'body',
        ['paragraph',
         ['plain', "Hello World"]]]
    result = markdown3.parse(data)
    assert expected == result

    expected = """
<p>Hello World</p>
    """.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_plain():
    data = "Name: Mr Flibble"
    expected = [
        'body',
        ['paragraph',
         ['plain', "Name: Mr Flibble"]]]
    result = markdown3.parse(data)
    assert expected == result

    expected = """
<p>Name: Mr Flibble</p>
    """.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_emphasis():
    data = "Hello *World*"
    expected = [
        'body',
        ['paragraph',
         ['plain', "Hello "],
         ['emphasis', "World"]]]
    result = markdown3.parse(data)
    assert expected == result

    expected = """
<p>Hello <strong>World</strong></p>
    """.strip()
    result = markdown3.to_html(data)
    assert expected == result

    data = "Text with *some bold* in it"
    expected = [
        'body',
        ['paragraph',
         ['plain', "Text with "],
         ['emphasis', "some bold"],
         ['plain', ' in it']]]
    result = markdown3.parse(data)
    assert expected == result

    expected = """
<p>Text with <strong>some bold</strong> in it</p>
    """.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_link():
    data = "[a link to Google with * in it](http://www.google.com)"
    expected = [
        'body',
        ['paragraph',
         ['link',
          ['link_text', "a link to Google with * in it"],
          ['link_url', "http://www.google.com"]]]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<p><a href="http://www.google.com">a link to Google with * in it</a></p>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    data = "Text with [a link to Google](http://www.google.com) in it"
    expected = [
        'body',
        ['paragraph',
         ['plain', "Text with "],
         ['link',
          ['link_text', "a link to Google"],
          ['link_url',
           "http://www.google.com"]],
         ['plain', " in it"]]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<p>Text with <a href="http://www.google.com">a link to Google</a> in it</p>
    '''.strip()

    result = markdown3.to_html(data)
    assert expected == result

def test_code():
    data = "text with `some code` in it"
    expected = [
        'body',
        ['paragraph',
         ['plain', "text with "],
         ['code', "some code"],
         ['plain', " in it"]]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<p>text with <code>some code</code> in it</p>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_paragraph():
    data = """
A paragraph.
"""
    expected = [
        'body',
        ['paragraph',
         ['plain', "A paragraph."]]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<p>A paragraph.</p>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    data = """
A paragraph with *some bold*, `some code` and [a link to Google](http://www.google.com) in it.
"""
    expected = [
        'body',
        ['paragraph',
         ['plain', "A paragraph with "],
         ['emphasis', "some bold"],
         ['plain', ", "],
         ['code', "some code"],
         ['plain', " and "],
         ['link',
          ['link_text', "a link to Google"],
          ['link_url', "http://www.google.com"]],
         ['plain', " in it."]]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<p>A paragraph with <strong>some bold</strong>, <code>some code</code> and <a href="http://www.google.com">a link to Google</a> in it.</p>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_title_level_1():
    data = """
# A level one title #
"""
    expected = [
        'body',
        ['title_level_1', "A level one title "]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<h1>A level one title </h1>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    # Without linebreaks
    data = """
# A level one title
""".strip()
    expected = [
        'body',
        ['title_level_1', "A level one title"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<h1>A level one title</h1>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    # With extra linebreaks

    data = """

# A level one title
"""
    expected = [
        'body',
        ['title_level_1', "A level one title"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<h1>A level one title</h1>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_title_level_2():
    data = """
## A level two title ##
"""
    expected = [
        'body',
        ['title_level_2', "A level two title "]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<h2>A level two title </h2>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    # Without linebreaks

    data = """
## A level two title
""".strip()
    expected = [
        'body',
        ['title_level_2', "A level two title"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<h2>A level two title</h2>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    # With extra linebreaks

    data = """

## A level two title
"""
    expected = [
        'body',
        ['title_level_2', "A level two title"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<h2>A level two title</h2>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_title_level_1_and_2():
    data = """
# A Header

## A SubHeader

"""

    expected = """
<h1>A Header</h1>

<h2>A SubHeader</h2>
    """.strip()

    result = markdown3.to_html(data)
    assert expected == result


class TestOrderedList(unittest.TestCase):
    """Test ordered lists
    """

    def test_simple(self):
        "Test that basic numbered bullets work"
        data = """
1. A numbered bullet
2. Another numbered bullet"""

        expected = [
            'body',
            ['ordered_list',
             ['numbered_bullet_without_paragraph',
              ['plain', "A numbered bullet"]],
             ['numbered_bullet_without_paragraph',
              ['plain', "Another numbered bullet"]]]]

        result = markdown3.parse(data)
        assert expected == result

        expected = '''
<ol>
  <li>A numbered bullet</li>
  <li>Another numbered bullet</li>
</ol>
        '''.strip()
        result = markdown3.to_html(data).strip()
        assert expected == result

    def test_with_tabs(self):
        "Test that tabs between the bullet and text work"
        data = """
1.	A numbered bullet
2.	Another numbered bullet"""

        expected = [
            'body',
            ['ordered_list',
             ['numbered_bullet_without_paragraph',
              ['plain', "A numbered bullet"]],
             ['numbered_bullet_without_paragraph',
              ['plain', "Another numbered bullet"]]]]

        result = markdown3.parse(data)
        assert expected == result

        expected = '''
<ol>
  <li>A numbered bullet</li>
  <li>Another numbered bullet</li>
</ol>
        '''.strip()
        result = markdown3.to_html(data).strip()
        assert expected == result

    def test_indented(self):
        "Test that an indented bullet works"
        data = """
    1. An indented numbered bullet"""

        expected = [
            'body',
            ['ordered_list',
             ['numbered_bullet_without_paragraph',
              ['plain', "An indented numbered bullet"]]]]

        result = markdown3.parse(data)
        assert expected == result

        expected = '''
<ol>
  <li>An indented numbered bullet</li>
</ol>
        '''.strip()
        result = markdown3.to_html(data)
        assert expected == result

    def test_multiple_bullets(self):
        "Test that several bullets with markup in them work"
        data = """
1. A numbered bullet
2. Another numbered bullet
3. A bullet with *bold*
4. A bullet with `code`
"""

        expected = [
            'body',
            ['ordered_list',
             ['numbered_bullet_without_paragraph',
              ['plain', "A numbered bullet"]],
             ['numbered_bullet_without_paragraph',
              ['plain', "Another numbered bullet"]],
             ['numbered_bullet_without_paragraph',
              ['plain', "A bullet with "],
              ['emphasis', "bold"]],
             ['numbered_bullet_without_paragraph',
              ['plain', "A bullet with "],
              ['code', "code"]]]]

        result = markdown3.parse(data)
        assert expected == result

        expected = '''
<ol>
  <li>A numbered bullet</li>
  <li>Another numbered bullet</li>
  <li>A bullet with <strong>bold</strong></li>
  <li>A bullet with <code>code</code></li>
</ol>
        '''.strip()

        result = markdown3.to_html(data)
        assert expected == result

    def test_paragraphs_in_bullet(self):
        "Test that spaced out bullets add paragraphs"
        data = """
1. A numbered bullet

2. Another numbered bullet

3. Yet another bullet
"""

        expected = [
            'body',
            ['ordered_list',
             ['numbered_bullet_with_paragraph',
              ['paragraph',
               ['plain', "A numbered bullet"]]],
             ['numbered_bullet_with_paragraph',
              ['paragraph',
               ['plain', "Another numbered bullet"]]],
             ['numbered_bullet_with_paragraph',
              ['paragraph',
               ['plain', "Yet another bullet"]]]]]

        result = markdown3.parse(data)
        assert expected == result

        expected = '''
<ol>
  <li><p>A numbered bullet</p></li>
  <li><p>Another numbered bullet</p></li>
  <li><p>Yet another bullet</p></li>
</ol>'''.strip()

        result = markdown3.to_html(data)
        assert expected == result

    def test_tab_indentation(self):
        data = """
	1. Bullet One
	2. Bullet Two"""

        expected = [
            'body',
            ['ordered_list',
             ['numbered_bullet_without_paragraph',
              ['plain', "Bullet One"]],
             ['numbered_bullet_without_paragraph',
              ['plain', "Bullet Two"]]]]

        result = markdown3.parse(data)
        assert expected == result

        expected = """
<ol>
  <li>Bullet One</li>
  <li>Bullet Two</li>
</ol>""".strip()
        result = markdown3.to_html(data)
        assert expected == result

    def test_multiple_paragraphs_bullet(self):
        data = """
1. Bullet One, Paragraph One
   Paragraph Two
""".strip()

        expected = [
            'numbered_bullet_with_paragraph',
              ['paragraph',
               ['plain',
                "Bullet One, Paragraph One"]],
              ['paragraph',
               ['plain',
               "Paragraph Two"]]]

        result = markdown3.parse(data, markdown3.numbered_bullet_with_paragraph)
        assert expected == result

        expected = """
<li><p>Bullet One, Paragraph One</p><p>Paragraph Two</p></li>
""".strip()
        result = markdown3.to_html(data, markdown3.numbered_bullet_with_paragraph)
        assert expected == result

    def test_multiple_paragraphs(self):
        data = """
1. Bullet One, Paragraph One
   Paragraph Two

2. Bullet Two
""".strip()

        expected = [
            'body',
            ['ordered_list',
             ['numbered_bullet_with_paragraph',
              ['paragraph',
               ['plain',
                "Bullet One, Paragraph One"]],
              ['paragraph',
               ['plain',
               "Paragraph Two"]]],
             ['numbered_bullet_with_paragraph',
              ['paragraph',
               ['plain',
               "Bullet Two"]]]]]

        result = markdown3.parse(data)
        assert expected == result

        expected = """
<ol>
  <li><p>Bullet One, Paragraph One</p><p>Paragraph Two</p></li>
  <li><p>Bullet Two</p></li>
</ol>
        """.strip()
        result = markdown3.to_html(data)
        assert expected == result


def test_unordered_list():
    def do_test(data, expected_tree, expected_html):
        result = markdown3.parse(data)
        assert expected_tree == result

        result = markdown3.to_html(data)
        assert expected_html == result

    items = [
        dict(
            expected_tree = [
                'body',
                ['unordered_list',
                 ['bullet_without_paragraph',
                  ['plain', "A bullet"]],
                 ['bullet_without_paragraph',
                  ['plain', "Another bullet"]]]],
            expected_html = '''
<ul>
  <li>A bullet</li>
  <li>Another bullet</li>
</ul>
        '''.strip(),
            data_templates = [
"""
%(bullet)s A bullet
%(bullet)s Another bullet""",
"""
%(bullet)s	A bullet
%(bullet)s	Another bullet""",
"""
  %(bullet)s A bullet
  %(bullet)s Another bullet"""]),
        dict(
            expected_tree = [
                'body',
                ['unordered_list',
                 ['bullet_with_paragraph',
                  ['paragraph',
                   ['plain', "A bullet"]]],
                 ['bullet_with_paragraph',
                  ['paragraph',
                   ['plain', "Another bullet"]]]]],
            expected_html = '''
<ul>
  <li><p>A bullet</p></li>
  <li><p>Another bullet</p></li>
</ul>
        '''.strip(),
            data_templates = [
"""
%(bullet)s A bullet

%(bullet)s Another bullet""",
"""
%(bullet)s	A bullet

%(bullet)s	Another bullet""",
"""
  %(bullet)s A bullet
  
  %(bullet)s Another bullet"""])]

    for item in items:
        expected_tree = item['expected_tree']
        expected_html = item['expected_html']
        data_templates = item['data_templates']
        for data_template in data_templates:
            for bullet_type in ["*", "-", "+"]:
                yield (do_test,
                       data_template % dict(bullet=bullet_type),
                       expected_tree,
                       expected_html)

def test_unordered_list_advanced():
    data = """
* A bullet
* Another bullet
* A bullet with *bold*
* A bullet with `code`
"""

    expected = [
        'body',
        ['unordered_list',
         ['bullet_without_paragraph',
          ['plain', "A bullet"]],
         ['bullet_without_paragraph',
          ['plain', "Another bullet"]],
         ['bullet_without_paragraph',
          ['plain', "A bullet with "],
          ['emphasis', "bold"]],
         ['bullet_without_paragraph',
          ['plain', "A bullet with "],
          ['code', "code"]]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<ul>
  <li>A bullet</li>
  <li>Another bullet</li>
  <li>A bullet with <strong>bold</strong></li>
  <li>A bullet with <code>code</code></li>
</ul>
    '''.strip()

    result = markdown3.to_html(data)
    assert expected == result


def test_nested_bullets():
    data = """
1. A numbered bullet
  2. A bullet in a sublist
  3. A bullet with *bold* in a sublist
4. A bullet with `code` in the first list
"""

    expected = [
        'body',
        ['ordered_list',
         ['numbered_bullet_without_paragraph',
          ['plain', "A numbered bullet"]],
         ['ordered_list_nested',
          ['numbered_bullet_without_paragraph',
           ['plain', "A bullet in a sublist"]],
          ['numbered_bullet_without_paragraph',
           ['plain', "A bullet with "],
           ['emphasis', "bold"],
           ['plain', " in a sublist"]]],
         ['numbered_bullet_without_paragraph',
          ['plain', "A bullet with "],
          ['code', "code"],
          ['plain', " in the first list"]]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = """
<ol>
  <li>A numbered bullet</li>
  <ol>
    <li>A bullet in a sublist</li>
    <li>A bullet with <strong>bold</strong> in a sublist</li>
  </ol>
  
  <li>A bullet with <code>code</code> in the first list</li>
</ol>
""".strip()

    result = markdown3.to_html(data)
    assert expected == result


def test_code_block():
    data = """
    <p>This is some html</p>"""

    expected = [
        'body',
        ['code_block',
         ['code_line',
          "&lt;p&gt;This is some html&lt;/p&gt;"]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = """
<code>
  &lt;p&gt;This is some html&lt;/p&gt;
</code>
    """.strip()

    result = markdown3.to_html(data)
    assert expected == result

    # Test list followed by code

    data = """

    1. A bullet point


    <p>This is some html</p>
"""

    expected = [
        'body',
        ['ordered_list',
         ['numbered_bullet_without_paragraph',
          ['plain', "A bullet point"]]],
        ['code_block',
         ['code_line',
          "&lt;p&gt;This is some html&lt;/p&gt;"]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = """
<ol>
  <li>A bullet point</li>
</ol>

<code>
  &lt;p&gt;This is some html&lt;/p&gt;
</code>
    """.strip()

    result = markdown3.to_html(data)
    assert expected == result


def test_horizontal_rules():
    data = """
---

- - - -

____

_ _ _ _ _

***

* * * *
"""

    expected = [
        'body',
        [ 'horizontal_rule', "---"],
        [ 'horizontal_rule', "- - -"],
        [ 'horizontal_rule', "___"],
        [ 'horizontal_rule', "_ _ _"],
        [ 'horizontal_rule', "***"],
        [ 'horizontal_rule', "* * *"]]

    result = markdown3.parse(data)
    assert expected == result

    expected = """
<hr/>

<hr/>

<hr/>

<hr/>

<hr/>

<hr/>

    """.strip()

    result = markdown3.to_html(data)
    assert expected == result


def test_quoted_paragraph():
    data = """
> A quoted paragraph
"""

    expected = [
        'body',
        ['blockquote',
         ['paragraph',
          ['plain',
           "A quoted paragraph"]]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = """
<blockquote>
  <p>A quoted paragraph</p>
  
</blockquote>
    """.strip()

    result = markdown3.to_html(data)
    assert expected == result

def test_document():
    data = """
# A Header

## A SubHeader ##

A paragraph with *some bold*, `some code` and [a link to Google](http://www.google.com) in it.

---

 1. A bullet in a list
 2. Another bullet
   * A sublist bullet
   * Another sublist bullet
 3. A bullet in the first list

  A code block with <span>some html</span> in it.

> A quoted paragraph
"""

    expected = """
<h1>A Header</h1>

<h2>A SubHeader </h2>

<p>A paragraph with <strong>some bold</strong>, <code>some code</code> and <a href="http://www.google.com">a link to Google</a> in it.</p>

<hr/>

<ol>
  <li>A bullet in a list</li>
  <li>Another bullet</li>
  <ul>
    <li>A sublist bullet</li>
    <li>Another sublist bullet</li>
  </ul>
  
  <li>A bullet in the first list</li>
</ol>

<code>
  A code block with &lt;span&gt;some html&lt;/span&gt; in it.
</code>

<blockquote>
  <p>A quoted paragraph</p>
  
</blockquote>
    """.strip()

    result = markdown3.to_html(data)
    assert expected == result
