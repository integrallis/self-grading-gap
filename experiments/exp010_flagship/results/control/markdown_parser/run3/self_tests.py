from solution import markdown_to_html

def test_empty_input():
    # Empty input produces an empty result — no HTML at all.
    assert markdown_to_html("") == ""

def test_plain_text():
    # A line of plain text renders as a paragraph: <p>text</p>.
    assert markdown_to_html("text") == "<p>text</p>"

def test_multiple_lines():
    # Each non-blank line yields exactly one block, and the blocks are joined by newlines.
    assert markdown_to_html("line 1\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_blank_lines():
    # Blank lines emit nothing: no empty paragraphs appear in the output.
    assert markdown_to_html("line 1\n\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_bold_text():
    # A span wrapped in double asterisks renders as strong emphasis inside its block: **bold** becomes <p><strong>bold</strong></p>.
    assert markdown_to_html("This is **bold** text.") == "<p>This is <strong>bold</strong> text.</p>"

def test_italic_text():
    # A span wrapped in single underscores renders as emphasis inside its block: _italic_ becomes <p><em>italic</em></p>.
    assert markdown_to_html("This is _italic_ text.") == "<p>This is <em>italic</em> text.</p>"

def test_nested_emphasis():
    # A bold span wrapping an italic span renders as <strong><em>...</em></strong>.
    assert markdown_to_html("This is **bold and _italic_** text.") == "<p>This is <strong>bold and <em>italic</em></strong> text.</p>"

def test_heading():
    # A line opening with one to six hashes followed by a space renders as <h1> through <h6>.
    assert markdown_to_html("# Heading 1") == "<h1>Heading 1</h1>"
    assert markdown_to_html("## Heading 2") == "<h2>Heading 2</h2>"
    assert markdown_to_html("### Heading 3") == "<h3>Heading 3</h3>"
    assert markdown_to_html("#### Heading 4") == "<h4>Heading 4</h4>"
    assert markdown_to_html("##### Heading 5") == "<h5>Heading 5</h5>"
    assert markdown_to_html("###### Heading 6") == "<h6>Heading 6</h6>"

def test_no_space_heading():
    # A hash not followed by a space is not a heading: it renders as an ordinary paragraph.
    assert markdown_to_html("#No space") == "<p>#No space</p>"

def test_too_many_hashes():
    # Seven or more hashes do not form a heading; it renders as an ordinary paragraph.
    assert markdown_to_html("####### Too many hashes") == "<p>####### Too many hashes</p>"

def test_heading_with_inline_emphasis():
    # Inline emphasis renders inside heading content.
    assert markdown_to_html("## This is _italic_ and **bold**") == "<h2>This is <em>italic</em> and <strong>bold</strong></h2>"

def test_link():
    # Link markup of the form [text](url) renders as an anchor: <a href="url">text</a>.
    assert markdown_to_html("This is a [link](http://example.com).") == "<p>This is a <a href=\"http://example.com\">link</a>.</p>"

def test_link_with_inline_emphasis():
    # Inline emphasis renders inside the link text.
    assert markdown_to_html("This is a [**bold link**](http://example.com).") == "<p>This is a <a href=\"http://example.com\"><strong>bold link</strong></a>.</p>"

def test_link_with_underscores_in_url():
    # Underscores inside a link URL are not emphasis markers: the URL passes through unchanged.
    assert markdown_to_html("This is a [link](http://example_com).") == "<p>This is a <a href=\"http://example_com\">link</a>.</p>"

def test_unordered_list():
    # A line of a dash and a space followed by text becomes a one-item unordered list.
    assert markdown_to_html("- item 1") == "<ul><li>item 1</li></ul>"

def test_consecutive_unordered_list_items():
    # Consecutive dash lines share a single <ul> wrapper.
    assert markdown_to_html("- item 1\n- item 2") == "<ul><li>item 1</li><li>item 2</li></ul>"

def test_blank_line_ends_list():
    # A blank line ends a list; a later dash line starts a new list of its own.
    assert markdown_to_html("- item 1\n\n- item 2") == "<ul><li>item 1</li></ul>\n<ul><li>item 2</li></ul>"

def test_dash_not_followed_by_space():
    # A dash not followed by a space is not a list item; it renders as an ordinary paragraph.
    assert markdown_to_html("-item 1") == "<p>-item 1</p>"

def test_non_dash_line_after_list():
    # A non-dash line immediately after a list closes the list and renders as its own block.
    assert markdown_to_html("- item 1\nThis is not a list item.") == "<ul><li>item 1</li></ul>\n<p>This is not a list item.</p>"

def test_inline_emphasis_in_list_items():
    # Inline emphasis renders inside list items.
    assert markdown_to_html("- This is **bold** in a list.") == "<ul><li>This is <strong>bold</strong> in a list.</li></ul>"