# -*- coding: utf-8 -*-

import py.test

import unittest

import markdown3, htmlise

class TestHeading1(unittest.TestCase):
    """General tests for heading_1"""

    def test_simple(self):
        """test simplest case"""
        datum = """# A level one heading #"""
        expected = [
            'body',
            ['heading_1', "A level one heading"]]
        result, rest = markdown3.parse(datum, with_rest=True)
        assert expected == result
        assert rest == ""

        expected_html = """<h1>A level one heading</h1>\n"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_without_closing_tag(self):
        """Test heading_1 without closing tag"""
        datum = """# A level one heading"""
        expected = [
            'body',
            ['heading_1', "A level one heading"]]
        result, rest = markdown3.parse(datum, with_rest=True)
        assert expected == result
        assert rest == ""

        expected_html = """<h1>A level one heading</h1>\n"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_with_leading_linebreaks(self):
        """Test heading_1 with leading linebreaks"""
        datum = """\n\n# A level one heading"""
        expected = [
            'body',
            ['heading_1', "A level one heading"]]
        result, rest = markdown3.parse(datum, with_rest=True)
        assert expected == result
        assert rest == ""

        expected_html = """<h1>A level one heading</h1>\n"""
        result = markdown3.to_html(datum)
        assert expected_html == result


class TestHeading2(unittest.TestCase):
    """General tests for heading_2"""

    def test_simple(self):
        """test simplest case"""
        datum = """## A level two heading ##"""
        expected = [
            'body',
            ['heading_2', "A level two heading"]]
        result, rest = markdown3.parse(datum, with_rest=True)
        assert expected == result
        assert rest == ""

        expected_html = """<h2>A level two heading</h2>\n"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_without_closing_tag(self):
        """Test heading_2 without closing tag"""
        datum = """## A level two heading"""
        expected = [
            'body',
            ['heading_2', "A level two heading"]]
        result, rest = markdown3.parse(datum, with_rest=True)
        assert expected == result
        assert rest == ""

        expected_html = """<h2>A level two heading</h2>\n"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_with_leading_linebreaks(self):
        """Test heading_2 with leading linebreaks"""
        datum = """\n\n## A level two heading"""
        expected = [
            'body',
            ['heading_2', "A level two heading"]]
        result, rest = markdown3.parse(datum, with_rest=True)
        assert expected == result
        assert rest == ""

        expected_html = """<h2>A level two heading</h2>\n"""
        result = markdown3.to_html(datum)
        assert expected_html == result


def test_linebreaks():
    """Check that body matches linebreaks"""
    datum = "\n\n"
    expected = ['body', ""]
    result, rest = markdown3.parse(datum, with_rest=True)
    assert expected == result
    assert rest == ""


class TestParagraph(unittest.TestCase):
    """General tests for paragraph"""

    def test_simple(self):
        """Simplest possible test"""
        datum = """A paragraph."""
        expected = [
            'body',
            ['paragraph',
             "A paragraph."]]
        result = markdown3.parse(datum)
        assert expected == result

        expected_html = """<p>A paragraph.</p>\n"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_multiline(self):
        """Test that a paragraph can contain single linebreaks"""
        datum = """A paragraph that spans\nmultiple lines."""
        expected = [
            'body',
            ['paragraph',
             "A paragraph that spans",
             " ",
             "multiple lines."]]
        result = markdown3.parse(datum)
        assert expected == result

        expected_html = """<p>A paragraph that spans multiple lines.</p>\n"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_paragraph_with_link(self):
        """Test that a link matches as part of a paragraph"""
        datum = "Some text with [a link to Google](http://www.google.com) in it."
        expected = [
            'body',
            ['paragraph',
             "Some text with",
             " ",
             ['link',
              ['link_text',
               "a link to Google"],
              ['link_url',
               "http://www.google.com"]],
             " ",
             "in it."]]
        result = markdown3.parse(datum)
        assert expected == result

        expected_html = """<p>Some text with <a href="http://www.google.com">a link to Google</a> in it.</p>\n"""
        result = markdown3.to_html(datum)
        assert expected_html == result


class TestUnorderedList(unittest.TestCase):
    """General tests for unordered list"""

    def test_simple(self):
        """Test simplest bulleted list"""
        datum = """
* item 1
* item 2
* item 3
""".strip()

        expected = [
            'body',
            ['unordered_list',
             ['unordered_bullet', "item 1"],
             ['unordered_bullet', "item 2"],
             ['unordered_bullet', "item 3"]]]

        result = markdown3.parse(datum)
        assert expected == result

        expected_html = """<ul>
  <li>
    item 1
  </li>
  <li>
    item 2
  </li>
  <li>
    item 3
  </li>
</ul>
"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_with_tabs(self):
        """Test bullet with tabs after bullet"""
        datum = """
*	item 1
*	item 2
*	item 3
""".strip()

        expected = [
            'body',
            ['unordered_list',
             ['unordered_bullet', "item 1"],
             ['unordered_bullet', "item 2"],
             ['unordered_bullet', "item 3"]]]

        result = markdown3.parse(datum)
        assert expected == result

        expected_html = """<ul>
  <li>
    item 1
  </li>
  <li>
    item 2
  </li>
  <li>
    item 3
  </li>
</ul>
"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_minus_with_tabs(self):
        """Test bullet with tabs after bullet"""
        datum = """
-	item 1
-	item 2
-	item 3
""".strip()

        expected = [
            'body',
            ['unordered_list',
             ['unordered_bullet', "item 1"],
             ['unordered_bullet', "item 2"],
             ['unordered_bullet', "item 3"]]]

        result = markdown3.parse(datum)
        assert expected == result

        expected_html = """<ul>
  <li>
    item 1
  </li>
  <li>
    item 2
  </li>
  <li>
    item 3
  </li>
</ul>
"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_multiple_paragraphs(self):
        """Test that a bullet can match multiple paragraphs"""
        def do_test(datum):
            expected = [
                'body',
                ['unordered_list',
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
                   "bullet three"]]]]
            result = markdown3.parse(datum)
            assert expected == result

            expected_html = """<ul>
  <li>
    <p>bullet one, paragraph one</p>
    <p>bullet one, paragraph two.  Spans multiple lines.</p>
  </li>
  <li>
    <p>bullet two</p>
  </li>
  <li>
    <p>bullet three</p>
  </li>
</ul>
"""
            result = markdown3.to_html(datum)
            assert expected_html == result

        data = [
"""
* bullet one, paragraph one

  bullet one, paragraph two.  Spans
  multiple lines.

* bullet two

* bullet three""".strip(),
"""
*	bullet one, paragraph one

	bullet one, paragraph two.  Spans
	multiple lines.

*	bullet two

*	bullet three""".strip()]

        for datum in data:
            do_test(datum)


class TestOrderedList(unittest.TestCase):
    """General tests for ordered list"""

    def test_simple(self):
        """Test simplest bulleted list"""
        datum = """
1. item 1
2. item 2
3. item 3
""".strip()

        expected = [
            'body',
            ['ordered_list',
             ['ordered_bullet', "item 1"],
             ['ordered_bullet', "item 2"],
             ['ordered_bullet', "item 3"]]]

        result = markdown3.parse(datum)
        assert expected == result

        expected_html = """<ol>
  <li>
    item 1
  </li>
  <li>
    item 2
  </li>
  <li>
    item 3
  </li>
</ol>
"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_with_tabs(self):
        """Test bullet with tabs after bullet"""
        datum = """
1.	item 1
2.	item 2
3.	item 3
""".strip()

        expected = [
            'body',
            ['ordered_list',
             ['ordered_bullet', "item 1"],
             ['ordered_bullet', "item 2"],
             ['ordered_bullet', "item 3"]]]

        result = markdown3.parse(datum)
        assert expected == result

        expected_html = """<ol>
  <li>
    item 1
  </li>
  <li>
    item 2
  </li>
  <li>
    item 3
  </li>
</ol>
"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_multiple_paragraphs(self):
        """Test that a bullet can match multiple paragraphs"""
        def do_test(datum):
            expected = [
                'body',
                ['ordered_list',
                 ['ordered_bullet',
                  ['paragraph',
                   "bullet one, paragraph one"],
                  ['paragraph',
                   "bullet one, paragraph two.  Spans",
                   " ",
                   "multiple lines."]],
                 ['ordered_bullet',
                  ['paragraph',
                   "bullet two"]],
                 ['ordered_bullet',
                  ['paragraph',
                   "bullet three"]]]]
            result = markdown3.parse(datum)
            assert expected == result

            expected_html = """<ol>
  <li>
    <p>bullet one, paragraph one</p>
    <p>bullet one, paragraph two.  Spans multiple lines.</p>
  </li>
  <li>
    <p>bullet two</p>
  </li>
  <li>
    <p>bullet three</p>
  </li>
</ol>
"""
            result = markdown3.to_html(datum)
            assert expected_html == result

        data = ["""
1. bullet one, paragraph one

   bullet one, paragraph two.  Spans
   multiple lines.

2. bullet two

3. bullet three""".strip(),
"""
1.	bullet one, paragraph one

	bullet one, paragraph two.  Spans
	multiple lines.

2.	bullet two

3.	bullet three""".strip(),
                ]

        for datum in data:
            do_test(datum)

    def test_nested_list_within_text(self):
        """Test that nested lists can be in text"""
        datum = """
1.	First
2.	Second:
	* Fee
	* Fie
	* Foe
3.	Third
        """.strip()
        expected = [
            'body',
            ['ordered_list',
             ['ordered_bullet',
              "First"],
             ['ordered_bullet',
              "Second:",
              ['unordered_list',
               ['unordered_bullet',
                "Fee"],
               ['unordered_bullet',
                "Fie"],
               ['unordered_bullet',
                "Foe"]]],
             ['ordered_bullet',
              "Third"]]]
        result = markdown3.parse(datum)
        assert expected == result

        expected_html = """<ol>
  <li>
    First
  </li>
  <li>
    Second:
    <ul>
      <li>
        Fee
      </li>
      <li>
        Fie
      </li>
      <li>
        Foe
      </li>
    </ul>
  </li>
  <li>
    Third
  </li>
</ol>
"""
        result = markdown3.to_html(datum)
        assert expected_html == result

    def test_multiple_paragraphs_with_nested_list(self):
        """Test that multiple paragraphs work with nested lists"""
        datum = """
1.	First

2.	Second:
	* Fee
	* Fie
	* Foe

3.	Third
        """.strip()
        expected = [
            'body',
            ['ordered_list',
             ['ordered_bullet',
              ['paragraph',
               "First"]],
             ['ordered_bullet',
              ['paragraph',
               "Second:"],
              ['unordered_list',
               ['unordered_bullet',
                "Fee"],
               ['unordered_bullet',
                "Fie"],
               ['unordered_bullet',
                "Foe"]]],
             ['ordered_bullet',
              ['paragraph',
               "Third"]]]]
        result = markdown3.parse(datum)
        assert expected == result

        expected_html = """<ol>
  <li>
    <p>First</p>
  </li>
  <li>
    <p>Second:</p>
    <ul>
      <li>
        Fee
      </li>
      <li>
        Fie
      </li>
      <li>
        Foe
      </li>
    </ul>
  </li>
  <li>
    <p>Third</p>
  </li>
</ol>
"""
        result = markdown3.to_html(datum)
        assert expected_html == result


def test_horizontal_rules():
    datum = """
---

- - - -

____

_ _ _ _ _

***

* * * *
"""

    expected = [
        'body',
        [ 'horizontal_rule', ""],
        [ 'horizontal_rule', ""],
        [ 'horizontal_rule', ""],
        [ 'horizontal_rule', ""],
        [ 'horizontal_rule', ""],
        [ 'horizontal_rule', ""]]

    result = markdown3.parse(datum)
    assert expected == result

    expected = """<hr/>

<hr/>

<hr/>

<hr/>

<hr/>

<hr/>
"""

    result = markdown3.to_html(datum)
    assert expected == result


# def test_title_level_1():
#     datum = """
# # A level one title #
# """
#     expected = [
#         'body',
#         ['title_level_1', "A level one title "]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <h1>A level one title </h1>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result

#     # Without linebreaks
#     datum = """
# # A level one title
# """.strip()
#     expected = [
#         'body',
#         ['title_level_1', "A level one title"]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <h1>A level one title</h1>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result

#     # With extra linebreaks

#     datum = """

# # A level one title
# """
#     expected = [
#         'body',
#         ['title_level_1', "A level one title"]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <h1>A level one title</h1>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result



# def test_body():
#     datum = "Hello World"
#     expected = [
#         'body',
#         ['paragraph',
#          ['plain', "Hello World"]]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = """
# <p>Hello World</p>
#     """.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result


# def test_plain():
#     datum = "Name: Mr Flibble"
#     expected = [
#         'body',
#         ['paragraph',
#          ['plain', "Name: Mr Flibble"]]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = """
# <p>Name: Mr Flibble</p>
#     """.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result


# def test_emphasis():
#     datum = "Hello *World*"
#     expected = [
#         'body',
#         ['paragraph',
#          ['plain', "Hello "],
#          ['emphasis', "World"]]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = """
# <p>Hello <strong>World</strong></p>
#     """.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result

#     datum = "Text with *some bold* in it"
#     expected = [
#         'body',
#         ['paragraph',
#          ['plain', "Text with "],
#          ['emphasis', "some bold"],
#          ['plain', ' in it']]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = """
# <p>Text with <strong>some bold</strong> in it</p>
#     """.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result


# def test_link():
#     datum = "[a link to Google with * in it](http://www.google.com)"
#     expected = [
#         'body',
#         ['paragraph',
#          ['link',
#           ['link_text', "a link to Google with * in it"],
#           ['link_url', "http://www.google.com"]]]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <p><a href="http://www.google.com">a link to Google with * in it</a></p>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result

#     datum = "Text with [a link to Google](http://www.google.com) in it"
#     expected = [
#         'body',
#         ['paragraph',
#          ['plain', "Text with "],
#          ['link',
#           ['link_text', "a link to Google"],
#           ['link_url',
#            "http://www.google.com"]],
#          ['plain', " in it"]]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <p>Text with <a href="http://www.google.com">a link to Google</a> in it</p>
#     '''.strip()

#     result = markdown3.to_html(datum)
#     assert expected == result

# def test_code():
#     datum = "text with `some code` in it"
#     expected = [
#         'body',
#         ['paragraph',
#          ['plain', "text with "],
#          ['code', "some code"],
#          ['plain', " in it"]]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <p>text with <code>some code</code> in it</p>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result


# def test_paragraph():
#     datum = """
# A paragraph.
# """
#     expected = [
#         'body',
#         ['paragraph',
#          ['plain', "A paragraph."]]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <p>A paragraph.</p>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result

#     datum = """
# A paragraph with *some bold*, `some code` and [a link to Google](http://www.google.com) in it.
# """
#     expected = [
#         'body',
#         ['paragraph',
#          ['plain', "A paragraph with "],
#          ['emphasis', "some bold"],
#          ['plain', ", "],
#          ['code', "some code"],
#          ['plain', " and "],
#          ['link',
#           ['link_text', "a link to Google"],
#           ['link_url', "http://www.google.com"]],
#          ['plain', " in it."]]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <p>A paragraph with <strong>some bold</strong>, <code>some code</code> and <a href="http://www.google.com">a link to Google</a> in it.</p>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result


# def test_title_level_1():
#     datum = """
# # A level one title #
# """
#     expected = [
#         'body',
#         ['title_level_1', "A level one title "]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <h1>A level one title </h1>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result

#     # Without linebreaks
#     datum = """
# # A level one title
# """.strip()
#     expected = [
#         'body',
#         ['title_level_1', "A level one title"]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <h1>A level one title</h1>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result

#     # With extra linebreaks

#     datum = """

# # A level one title
# """
#     expected = [
#         'body',
#         ['title_level_1', "A level one title"]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <h1>A level one title</h1>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result


# def test_title_level_2():
#     datum = """
# ## A level two title ##
# """
#     expected = [
#         'body',
#         ['title_level_2', "A level two title "]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <h2>A level two title </h2>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result

#     # Without linebreaks

#     datum = """
# ## A level two title
# """.strip()
#     expected = [
#         'body',
#         ['title_level_2', "A level two title"]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <h2>A level two title</h2>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result

#     # With extra linebreaks

#     datum = """

# ## A level two title
# """
#     expected = [
#         'body',
#         ['title_level_2', "A level two title"]]
#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <h2>A level two title</h2>
#     '''.strip()
#     result = markdown3.to_html(datum)
#     assert expected == result


# def test_title_level_1_and_2():
#     datum = """
# # A Header

# ## A SubHeader

# """

#     expected = """
# <h1>A Header</h1>

# <h2>A SubHeader</h2>
#     """.strip()

#     result = markdown3.to_html(datum)
#     assert expected == result


# class TestOrderedList(unittest.TestCase):
#     """Test ordered lists
#     """

#     def test_simple(self):
#         "Test that basic numbered bullets work"
#         datum = """
# 1. A numbered bullet
# 2. Another numbered bullet"""

#         expected = [
#             'body',
#             ['ordered_list',
#              ['numbered_bullet_without_paragraph',
#               ['plain', "A numbered bullet"]],
#              ['numbered_bullet_without_paragraph',
#               ['plain', "Another numbered bullet"]]]]

#         result = markdown3.parse(datum)
#         assert expected == result

#         expected = '''
# <ol>
#   <li>A numbered bullet</li>
#   <li>Another numbered bullet</li>
# </ol>
#         '''.strip()
#         result = markdown3.to_html(datum).strip()
#         assert expected == result

#     def test_with_tabs(self):
#         "Test that tabs between the bullet and text work"
#         datum = """
# 1.	A numbered bullet
# 2.	Another numbered bullet"""

#         expected = [
#             'body',
#             ['ordered_list',
#              ['numbered_bullet_without_paragraph',
#               ['plain', "A numbered bullet"]],
#              ['numbered_bullet_without_paragraph',
#               ['plain', "Another numbered bullet"]]]]

#         result = markdown3.parse(datum)
#         assert expected == result

#         expected = '''
# <ol>
#   <li>A numbered bullet</li>
#   <li>Another numbered bullet</li>
# </ol>
#         '''.strip()
#         result = markdown3.to_html(datum).strip()
#         assert expected == result

#     def test_indented(self):
#         "Test that an indented bullet works"
#         datum = """
#     1. An indented numbered bullet"""

#         expected = [
#             'body',
#             ['ordered_list',
#              ['numbered_bullet_without_paragraph',
#               ['plain', "An indented numbered bullet"]]]]

#         result = markdown3.parse(datum)
#         assert expected == result

#         expected = '''
# <ol>
#   <li>An indented numbered bullet</li>
# </ol>
#         '''.strip()
#         result = markdown3.to_html(datum)
#         assert expected == result

#     def test_multiple_bullets(self):
#         "Test that several bullets with markup in them work"
#         datum = """
# 1. A numbered bullet
# 2. Another numbered bullet
# 3. A bullet with *bold*
# 4. A bullet with `code`
# """

#         expected = [
#             'body',
#             ['ordered_list',
#              ['numbered_bullet_without_paragraph',
#               ['plain', "A numbered bullet"]],
#              ['numbered_bullet_without_paragraph',
#               ['plain', "Another numbered bullet"]],
#              ['numbered_bullet_without_paragraph',
#               ['plain', "A bullet with "],
#               ['emphasis', "bold"]],
#              ['numbered_bullet_without_paragraph',
#               ['plain', "A bullet with "],
#               ['code', "code"]]]]

#         result = markdown3.parse(datum)
#         assert expected == result

#         expected = '''
# <ol>
#   <li>A numbered bullet</li>
#   <li>Another numbered bullet</li>
#   <li>A bullet with <strong>bold</strong></li>
#   <li>A bullet with <code>code</code></li>
# </ol>
#         '''.strip()

#         result = markdown3.to_html(datum)
#         assert expected == result

#     def test_paragraphs_in_bullet(self):
#         "Test that spaced out bullets add paragraphs"
#         datum = """
# 1. A numbered bullet

# 2. Another numbered bullet

# 3. Yet another bullet
# """

#         expected = [
#             'body',
#             ['ordered_list',
#              ['numbered_bullet_with_paragraph',
#               ['paragraph',
#                ['plain', "A numbered bullet"]]],
#              ['numbered_bullet_with_paragraph',
#               ['paragraph',
#                ['plain', "Another numbered bullet"]]],
#              ['numbered_bullet_with_paragraph',
#               ['paragraph',
#                ['plain', "Yet another bullet"]]]]]

#         result = markdown3.parse(datum)
#         assert expected == result

#         expected = '''
# <ol>
#   <li><p>A numbered bullet</p></li>
#   <li><p>Another numbered bullet</p></li>
#   <li><p>Yet another bullet</p></li>
# </ol>'''.strip()

#         result = markdown3.to_html(datum)
#         assert expected == result

#     def test_tab_indentation_with_multiple_paragraphs(self):
#         datum = """
# 1.	Bullet One, Paragraph One

# 	Paragraph Two

# 2.	Bullet Two

# 3.	Bullet Three
# """

#         expected = [
#             'body',
#             ['ordered_list',
#              ['numbered_bullet_with_paragraph',
#               ['paragraph',
#                ['plain', "Bullet One, Paragraph One"]],
#               ['paragraph',
#                ['plain', "Paragraph Two"]]],
#              ['numbered_bullet_with_paragraph',
#               ['paragraph',
#                ['plain', "Bullet Two"]]],
#              ['numbered_bullet_with_paragraph',
#               ['paragraph',
#                ['plain', "Bullet Three"]]]]]

#         result = markdown3.parse(datum)
#         assert expected == result

#         expected = """
# <ol>
#   <li><p>Bullet One, Paragraph One</p><p>Paragraph Two</p></li>
#   <li><p>Bullet Two</p></li>
#   <li><p>Bullet Three</p></li>
# </ol>""".strip()
#         result = markdown3.to_html(datum)
#         assert expected == result

#     def test_tab_indentation(self):
#         datum = """
# 	1. Bullet One
# 	2. Bullet Two"""

#         expected = [
#             'body',
#             ['ordered_list',
#              ['numbered_bullet_without_paragraph',
#               ['plain', "Bullet One"]],
#              ['numbered_bullet_without_paragraph',
#               ['plain', "Bullet Two"]]]]

#         result = markdown3.parse(datum)
#         assert expected == result

#         expected = """
# <ol>
#   <li>Bullet One</li>
#   <li>Bullet Two</li>
# </ol>""".strip()
#         result = markdown3.to_html(datum)
#         assert expected == result

#     def test_multiple_paragraphs_bullet(self):
#         datum = """
# 1. Bullet One, Paragraph One
#    Paragraph Two
# """.strip()

#         expected = [
#             'numbered_bullet_with_paragraph',
#               ['paragraph',
#                ['plain',
#                 "Bullet One, Paragraph One"]],
#               ['paragraph',
#                ['plain',
#                "Paragraph Two"]]]

#         result = markdown3.parse(datum, markdown3.numbered_bullet_with_paragraph)
#         assert expected == result

#         expected = """
# <li><p>Bullet One, Paragraph One</p><p>Paragraph Two</p></li>
# """.strip()
#         result = markdown3.to_html(datum, markdown3.numbered_bullet_with_paragraph)
#         assert expected == result

#     def test_multiple_paragraphs(self):
#         datum = """
# 1. Bullet One, Paragraph One
#    Paragraph Two

# 2. Bullet Two
# """.strip()

#         expected = [
#             'body',
#             ['ordered_list',
#              ['numbered_bullet_with_paragraph',
#               ['paragraph',
#                ['plain',
#                 "Bullet One, Paragraph One"]],
#               ['paragraph',
#                ['plain',
#                "Paragraph Two"]]],
#              ['numbered_bullet_with_paragraph',
#               ['paragraph',
#                ['plain',
#                "Bullet Two"]]]]]

#         result = markdown3.parse(datum)
#         assert expected == result

#         expected = """
# <ol>
#   <li><p>Bullet One, Paragraph One</p><p>Paragraph Two</p></li>
#   <li><p>Bullet Two</p></li>
# </ol>
#         """.strip()
#         result = markdown3.to_html(datum)
#         assert expected == result


# def test_unordered_list():
#     def do_test(datum, expected_tree, expected_html):
#         result = markdown3.parse(datum)
#         assert expected_tree == result

#         result = markdown3.to_html(datum)
#         assert expected_html == result

#     items = [
#         dict(
#             expected_tree = [
#                 'body',
#                 ['unordered_list',
#                  ['bullet_without_paragraph',
#                   ['plain', "A bullet"]],
#                  ['bullet_without_paragraph',
#                   ['plain', "Another bullet"]]]],
#             expected_html = '''
# <ul>
#   <li>A bullet</li>
#   <li>Another bullet</li>
# </ul>
#         '''.strip(),
#             datum_templates = [
# """
# %(bullet)s A bullet
# %(bullet)s Another bullet""",
# """
# %(bullet)s	A bullet
# %(bullet)s	Another bullet""",
# """
#   %(bullet)s A bullet
#   %(bullet)s Another bullet"""]),
#         dict(
#             expected_tree = [
#                 'body',
#                 ['unordered_list',
#                  ['bullet_with_paragraph',
#                   ['paragraph',
#                    ['plain', "A bullet"]]],
#                  ['bullet_with_paragraph',
#                   ['paragraph',
#                    ['plain', "Another bullet"]]]]],
#             expected_html = '''
# <ul>
#   <li><p>A bullet</p></li>
#   <li><p>Another bullet</p></li>
# </ul>
#         '''.strip(),
#             datum_templates = [
# """
# %(bullet)s A bullet

# %(bullet)s Another bullet""",
# """
# %(bullet)s	A bullet

# %(bullet)s	Another bullet""",
# """
#   %(bullet)s A bullet
  
#   %(bullet)s Another bullet"""])]

#     for item in items:
#         expected_tree = item['expected_tree']
#         expected_html = item['expected_html']
#         datum_templates = item['datum_templates']
#         for datum_template in datum_templates:
#             for bullet_type in ["*", "-", "+"]:
#                 yield (do_test,
#                        datum_template % dict(bullet=bullet_type),
#                        expected_tree,
#                        expected_html)

# def test_unordered_list_advanced():
#     datum = """
# * A bullet
# * Another bullet
# * A bullet with *bold*
# * A bullet with `code`
# """

#     expected = [
#         'body',
#         ['unordered_list',
#          ['bullet_without_paragraph',
#           ['plain', "A bullet"]],
#          ['bullet_without_paragraph',
#           ['plain', "Another bullet"]],
#          ['bullet_without_paragraph',
#           ['plain', "A bullet with "],
#           ['emphasis', "bold"]],
#          ['bullet_without_paragraph',
#           ['plain', "A bullet with "],
#           ['code', "code"]]]]

#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = '''
# <ul>
#   <li>A bullet</li>
#   <li>Another bullet</li>
#   <li>A bullet with <strong>bold</strong></li>
#   <li>A bullet with <code>code</code></li>
# </ul>
#     '''.strip()

#     result = markdown3.to_html(datum)
#     assert expected == result


# def test_nested_bullets():
#     datum = """
# 1. A numbered bullet
#   2. A bullet in a sublist
#   3. A bullet with *bold* in a sublist
# 4. A bullet with `code` in the first list
# """

#     expected = [
#         'body',
#         ['ordered_list',
#          ['numbered_bullet_without_paragraph',
#           ['plain', "A numbered bullet"]],
#          ['ordered_list_nested',
#           ['numbered_bullet_without_paragraph',
#            ['plain', "A bullet in a sublist"]],
#           ['numbered_bullet_without_paragraph',
#            ['plain', "A bullet with "],
#            ['emphasis', "bold"],
#            ['plain', " in a sublist"]]],
#          ['numbered_bullet_without_paragraph',
#           ['plain', "A bullet with "],
#           ['code', "code"],
#           ['plain', " in the first list"]]]]

#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = """
# <ol>
#   <li>A numbered bullet</li>
#   <ol>
#     <li>A bullet in a sublist</li>
#     <li>A bullet with <strong>bold</strong> in a sublist</li>
#   </ol>
  
#   <li>A bullet with <code>code</code> in the first list</li>
# </ol>
# """.strip()

#     result = markdown3.to_html(datum)
#     assert expected == result


# def test_code_block():
#     datum = """
#     <p>This is some html</p>"""

#     expected = [
#         'body',
#         ['code_block',
#          ['code_line',
#           "&lt;p&gt;This is some html&lt;/p&gt;"]]]

#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = """
# <code>
#   &lt;p&gt;This is some html&lt;/p&gt;
# </code>
#     """.strip()

#     result = markdown3.to_html(datum)
#     assert expected == result

#     # Test list followed by code

#     datum = """

#     1. A bullet point


#     <p>This is some html</p>
# """

#     expected = [
#         'body',
#         ['ordered_list',
#          ['numbered_bullet_without_paragraph',
#           ['plain', "A bullet point"]]],
#         ['code_block',
#          ['code_line',
#           "&lt;p&gt;This is some html&lt;/p&gt;"]]]

#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = """
# <ol>
#   <li>A bullet point</li>
# </ol>

# <code>
#   &lt;p&gt;This is some html&lt;/p&gt;
# </code>
#     """.strip()

#     result = markdown3.to_html(datum)
#     assert expected == result



# def test_quoted_paragraph():
#     datum = """
# > A quoted paragraph
# """

#     expected = [
#         'body',
#         ['blockquote',
#          ['paragraph',
#           ['plain',
#            "A quoted paragraph"]]]]

#     result = markdown3.parse(datum)
#     assert expected == result

#     expected = """
# <blockquote>
#   <p>A quoted paragraph</p>
  
# </blockquote>
#     """.strip()

#     result = markdown3.to_html(datum)
#     assert expected == result

# def test_document():
#     datum = """
# # A Header

# ## A SubHeader ##

# A paragraph with *some bold*, `some code` and [a link to Google](http://www.google.com) in it.

# ---

#  1. A bullet in a list
#  2. Another bullet
#    * A sublist bullet
#    * Another sublist bullet
#  3. A bullet in the first list

#   A code block with <span>some html</span> in it.

# > A quoted paragraph
# """

#     expected = """
# <h1>A Header</h1>

# <h2>A SubHeader </h2>

# <p>A paragraph with <strong>some bold</strong>, <code>some code</code> and <a href="http://www.google.com">a link to Google</a> in it.</p>

# <hr/>

# <ol>
#   <li>A bullet in a list</li>
#   <li>Another bullet</li>
#   <ul>
#     <li>A sublist bullet</li>
#     <li>Another sublist bullet</li>
#   </ul>
  
#   <li>A bullet in the first list</li>
# </ol>

# <code>
#   A code block with &lt;span&gt;some html&lt;/span&gt; in it.
# </code>

# <blockquote>
#   <p>A quoted paragraph</p>
  
# </blockquote>
#     """.strip()

#     result = markdown3.to_html(datum)
#     assert expected == result
