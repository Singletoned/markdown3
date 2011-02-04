# -*- coding: utf-8 -*-

import markdown3

def test_body():
    data = "Hello World"
    expected = ['body', ['plain', "Hello World"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = """
<body>
  Hello World
</body>
    """.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_emphasis():
    data = "Hello *World*"
    expected = [
        'body',
        ['plain', "Hello "],
        ['emphasis', "World"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = """
<body>
  Hello 
  <strong>World</strong>
</body>
    """.strip()
    result = markdown3.to_html(data)
    assert expected == result

    data = "Text with *some bold* in it"
    expected = [
        'body',
        ['plain', "Text with "],
        ['emphasis', "some bold"],
        ['plain', ' in it']]
    result = markdown3.parse(data)
    assert expected == result

    expected = """
<body>
  Text with 
  <strong>some bold</strong>
   in it
</body>
    """.strip()
    result = markdown3.to_html(data)
    assert expected == result


def test_link():
    data = "[a link to Google](http://www.google.com)"
    expected = [
        'link',
        ['link_text', "a link to Google"],
        ['link_url',
         ['', "http://www.google.com"]]]
    result = markdown3.pg.parse_string(data, markdown3.link)
    assert expected == result

    expected = '''
<body>
  <a href="http://www.google.com">a link to Google</a>
</body>
    '''.strip()
    result = markdown3.to_html(data)
    assert expected == result

    data = "Text with [a link to Google](http://www.google.com) in it"
    expected = [
        'body',
        ['plain', "Text with "],
        ['link',
         ['link_text', "a link to Google"],
         ['link_url',
          ['', "http://www.google.com"]]],
        ['plain', " in it"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  Text with
  <a href="http://ww.google.com">
    a link to Google
  </a>
</body>
    '''.strip()


def test_code():
    data = "text with `some code` in it"
    expected = [
        'body',
        ['plain', "text with "],
        ['code',
         ['', "some code"]],
        ['plain', " in it"]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  text with 
  <code>some code</code>
   in it
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
         ['',
          ['',
           ['plain', "A paragraph."]]]]]
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
         ['',
          ['',
           ['plain', "A paragraph with "],
           ['emphasis', "some bold"],
           ['plain', ", "],
           ['code',
            ['', "some code"]],
           ['plain', " and "],
           ['link',
            ['link_text', "a link to Google"],
            ['link_url',
             ['', "http://www.google.com"]]],
           ['plain', " in it."]]]]]
    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <p>
    A paragraph with 
    <strong>some bold</strong>
    , 
    <code>some code</code>
     and 
    <a href="http://www.google.com">a link to Google</a>
     in it.
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


def test_ordered_list():
    data = """
1. A numbered bullet"""

    expected = [
        'body',
        ['ordered_list',
         ['numbered_bullet',
          ['',
           ['',
            ['plain', "A numbered bullet"]]]]]]

    result = markdown3.parse(data)
    assert expected == result

    expected = '''
<body>
  <ol>
    <li>
      A numbered bullet
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
          ['',
           ['',
            ['plain', "A numbered bullet"]]]],
         ['',
          ['numbered_bullet',
           ['',
            ['',
             ['plain', "Another numbered bullet"]]]],
          ['numbered_bullet',
           ['',
            ['',
             ['plain', "A bullet with "],
            ['emphasis', "bold"]]]],
          ['numbered_bullet',
           ['',
            ['',
             ['plain', "A bullet with "],
            ['code',
             ['', "code"]]]]]]]]

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
      A bullet with 
      <strong>bold</strong>
    </li>
    <li>
      A bullet with 
      <code>code</code>
    </li>
  </ol>
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
          ['',
           ['',
            ['plain', "A numbered bullet"]]]],
         ['',
          ['ordered_list',
           ['numbered_bullet',
            ['',
             ['',
              ['plain', "A bullet in a sublist"]]]],
           ['',
            ['numbered_bullet',
             ['',
              ['',
               ['plain', "A bullet with "],
              ['emphasis', "bold"],
              ['plain', " in a sublist"]]]]]],
          ['numbered_bullet',
           ['',
            ['',
             ['plain', "A bullet with "],
            ['code',
             ['', "code"]],
            ['plain', " in the first list"]]]]]]]

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
        A bullet with 
        <strong>bold</strong>
         in a sublist
      </li>
    </ol>
    <li>
      A bullet with 
      <code>code</code>
       in the first list
    </li>
  </ol>
</body>""".strip()

    result = markdown3.to_html(data)
    assert expected == result
