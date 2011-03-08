# -*- coding: utf-8 -*-

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
<body>
  <p>
    Hello World
  </p>
</body>
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
<body>
  <p>
    Hello <strong>World</strong>
  </p>
</body>
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
<body>
  <p>
    Text with <strong>some bold</strong> in it
  </p>
</body>
    """.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_link():
    data = "[a link to Google](http://www.google.com)"
    expected = [
        'body',
        ['paragraph',
         ['link',
          ['link_text', "a link to Google"],
          ['link_url', "http://www.google.com"]]]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <p>
    <a href="http://www.google.com">a link to Google</a>
  </p>
</body>
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
<body>
  Text with <a href="http://ww.google.com"> a link to Google </a>
</body>
    '''.strip()


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
<body>
  <p>
    text with <code>some code</code> in it
  </p>
</body>
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
<body>
  <p>
    A paragraph.
  </p>
</body>
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
<body>
  <p>
    A paragraph with <strong>some bold</strong>, <code>some code</code> and <a href="http://www.google.com">a link to Google</a> in it.
  </p>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_title_level_1():
    data = """
# A level one title #
"""
    expected = [
        'body',
        ['title_level_1', " A level one title "]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <h1>
     A level one title 
  </h1>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    data = """
# A level one title
"""
    expected = [
        'body',
        ['title_level_1', " A level one title"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <h1>
     A level one title
  </h1>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    # With extra linebreaks

    data = """

# A level one title
"""
    expected = [
        'body',
        ['title_level_1', " A level one title"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <h1>
     A level one title
  </h1>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_title_level_2():
    data = """
## A level two title ##
"""
    expected = [
        'body',
        ['title_level_2', " A level two title "]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <h2>
     A level two title 
  </h2>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    data = """
## A level two title
"""
    expected = [
        'body',
        ['title_level_2', " A level two title"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <h2>
     A level two title
  </h2>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    # With extra linebreaks

    data = """

## A level two title
"""
    expected = [
        'body',
        ['title_level_2', " A level two title"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <h2>
     A level two title
  </h2>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_title_level_1_and_2():
    data = """
# A Header

## A SubHeader

"""

    expected = """
<body>
  <h1>
     A Header
  </h1>
  <h2>
     A SubHeader
  </h2>
</body>
    """.strip()

    result = markdown3.to_html(data)
    assert expected == result


def test_ordered_list():
    data = """
1. A numbered bullet
2. Another numbered bullet"""

    expected = [
        'body',
        ['ordered_list',
         ['numbered_bullet',
          ['plain', "A numbered bullet"]],
         ['numbered_bullet',
          ['plain', "Another numbered bullet"]]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <ol>
    <li>
      A numbered bullet
    </li>
    <li>
      Another numbered bullet
    </li>
  </ol>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    data = """
  1. An indented numbered bullet"""

    expected = [
        'body',
        ['ordered_list',
         ['numbered_bullet',
          ['plain', "An indented numbered bullet"]]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <ol>
    <li>
      An indented numbered bullet
    </li>
  </ol>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result


    data = """
1. A numbered bullet
2. Another numbered bullet
3. A bullet with *bold*
4. A bullet with `code`
"""

    expected = [
        'body',
        ['ordered_list',
         ['numbered_bullet',
          ['plain', "A numbered bullet"]],
         ['numbered_bullet',
          ['plain', "Another numbered bullet"]],
         ['numbered_bullet',
          ['plain', "A bullet with "],
          ['emphasis', "bold"]],
         ['numbered_bullet',
          ['plain', "A bullet with "],
          ['code', "code"]]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <ol>
    <li>
      A numbered bullet
    </li>
    <li>
      Another numbered bullet
    </li>
    <li>
      A bullet with <strong>bold</strong>
    </li>
    <li>
      A bullet with <code>code</code>
    </li>
  </ol>
</body>
    '''.strip()

    result = markdown3.to_html(data)
    assert expected == result


def test_unordered_list():
    data = """
* A bullet
* Another bullet"""

    expected = [
        'body',
        ['unordered_list',
         ['bullet',
          ['plain', "A bullet"]],
         ['bullet',
          ['plain', "Another bullet"]]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <ul>
    <li>
      A bullet
    </li>
    <li>
      Another bullet
    </li>
  </ul>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    data = """
  * An indented bullet"""

    expected = [
        'body',
        ['unordered_list',
         ['bullet',
          ['plain', "An indented bullet"]]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <ul>
    <li>
      An indented bullet
    </li>
  </ul>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result


    data = """
* A bullet
* Another bullet
* A bullet with *bold*
* A bullet with `code`
"""

    expected = [
        'body',
        ['unordered_list',
         ['bullet',
          ['plain', "A bullet"]],
         ['bullet',
          ['plain', "Another bullet"]],
         ['bullet',
          ['plain', "A bullet with "],
          ['emphasis', "bold"]],
         ['bullet',
          ['plain', "A bullet with "],
          ['code', "code"]]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <ul>
    <li>
      A bullet
    </li>
    <li>
      Another bullet
    </li>
    <li>
      A bullet with <strong>bold</strong>
    </li>
    <li>
      A bullet with <code>code</code>
    </li>
  </ul>
</body>
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
         ['numbered_bullet',
          ['plain', "A numbered bullet"]],
         ['ordered_list',
          ['numbered_bullet',
           ['plain', "A bullet in a sublist"]],
          ['numbered_bullet',
           ['plain', "A bullet with "],
           ['emphasis', "bold"],
           ['plain', " in a sublist"]]],
         ['numbered_bullet',
          ['plain', "A bullet with "],
          ['code', "code"],
          ['plain', " in the first list"]]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = """
<body>
  <ol>
    <li>
      A numbered bullet
    </li>
    <ol>
      <li>
        A bullet in a sublist
      </li>
      <li>
        A bullet with <strong>bold</strong> in a sublist
      </li>
    </ol>
    <li>
      A bullet with <code>code</code> in the first list
    </li>
  </ol>
</body>""".strip()

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
<body>
  <code>
    &lt;p&gt;This is some html&lt;/p&gt;
  </code>
</body>
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
         ['numbered_bullet',
          ['plain', "A bullet point"]]],
        ['code_block',
         ['code_line',
          "&lt;p&gt;This is some html&lt;/p&gt;"]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = """
<body>
  <ol>
    <li>
      A bullet point
    </li>
  </ol>
  <code>
    &lt;p&gt;This is some html&lt;/p&gt;
  </code>
</body>
    """.strip()

    result = markdown3.to_html(data)
    assert expected == result


def test_horizontal_rules():
    data = """
---
"""

    expected = [
        'body',
        [ 'horizontal_rule', ""]]

    result = markdown3.parse(data)
    assert expected == result

    expected = """
<body>
  <hr/>
</body>
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
"""

    expected = """
<body>
  <h1>
     A Header
  </h1>
  <h2>
     A SubHeader 
  </h2>
  <p>
    A paragraph with <strong>some bold</strong>, <code>some code</code> and <a href="http://www.google.com">a link to Google</a> in it.
  </p>
  <hr/>
  <ol>
    <li>
      A bullet in a list
    </li>
    <li>
      Another bullet
    </li>
    <ul>
      <li>
        A sublist bullet
      </li>
      <li>
        Another sublist bullet
      </li>
    </ul>
    <li>
      A bullet in the first list
    </li>
  </ol>
  <code>
    A code block with &lt;span&gt;some html&lt;/span&gt; in it.
  </code>
</body>
    """.strip()

    result = markdown3.to_html(data)
    assert expected == result
