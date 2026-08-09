def test_empty_input():
    # Empty input produces an empty result — no HTML at all.
    assert markdown_to_html("") == ""

def test_plain_text():
    # A line of plain text renders as a paragraph: <p>text</p>.
    assert markdown_to_html("text") == "<p>text</p>"

def test_non_blank_lines_yield_blocks():
    # Each non-blank line yields exactly one block, and the blocks are joined by newlines.
    assert markdown_to_html("line 1\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_blank_lines_emit_nothing():
    # Blank lines emit nothing: no empty paragraphs appear in the output.
    assert markdown_to_html("line 1\n\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_bold_rendering():
    # A span wrapped in double asterisks renders as strong emphasis: **bold** becomes <p><strong>bold</strong></p>.
    assert markdown_to_html("**bold**") == "<p><strong>bold</strong></p>"

def test_italic_rendering():
    # A span wrapped in single underscores renders as emphasis: _italic_ becomes <p><em>italic</em></p>.
    assert markdown_to_html("_italic_") == "<p><em>italic</em></p>"

def test_nested_bold_and_italic():
    # A bold span wrapping an italic span renders as <strong><em>...</em></strong>.
    assert markdown_to_html("**bold _italic_**") == "<p><strong>bold <em>italic</em></strong></p>"

def test_inline_markup_leaves_plain_text_untouched():
    # Inline markup renders in place, leaving surrounding plain text untouched.
    assert markdown_to_html("This is **bold** and _italic_.") == "<p>This is <strong>bold</strong> and <em>italic</em>.</p>"

def test_heading_with_hashes():
    # A line opening with one to six hashes renders as <h1> through <h6>.
    assert markdown_to_html("# Heading 1") == "<h1>Heading 1</h1>"
    assert markdown_to_html("## Heading 2") == "<h2>Heading 2</h2>"
    assert markdown_to_html("### Heading 3") == "<h3>Heading 3</h3>"
    assert markdown_to_html("#### Heading 4") == "<h4>Heading 4</h4>"
    assert markdown_to_html("##### Heading 5") == "<h5>Heading 5</h5>"
    assert markdown_to_html("###### Heading 6") == "<h6>Heading 6</h6>"

def test_heading_no_space():
    # A hash not followed by a space is not a heading: renders as a paragraph.
    assert markdown_to_html("#No space") == "<p>#No space</p>"

def test_too_many_hashes_not_a_heading():
    # Seven or more hashes do not form a heading; render as ordinary paragraph.
    assert markdown_to_html("####### Too many hashes") == "<p>####### Too many hashes</p>"

def test_heading_with_inline_emphasis():
    # Inline emphasis renders inside heading content.
    assert markdown_to_html("## **Bold Heading**") == "<h2><strong>Bold Heading</strong></h2>"

def test_link_rendering():
    # Link markup of the form [text](url) renders as <a href="url">text</a>.
    assert markdown_to_html("[example](http://example.com)") == "<p><a href=\"http://example.com\">example</a></p>"

def test_link_inline_rendering():
    # A link renders in place within its surrounding text.
    assert markdown_to_html("This is a [link](http://example.com).") == "<p>This is a <a href=\"http://example.com\">link</a>.</p>"

def test_link_with_underscores():
    # Underscores inside a link URL are not emphasis markers.
    assert markdown_to_html("[example_link](http://example_link.com)") == "<p><a href=\"http://example_link.com\">example_link</a></p>"

def test_link_with_inline_emphasis():
    # Inline emphasis renders inside the link text.
    assert markdown_to_html("[This is _italic_](http://example.com)") == "<p><a href=\"http://example.com\">This is <em>italic</em></a></p>"

def test_unordered_list_single_item():
    # A line of a dash and space becomes a one-item unordered list.
    assert markdown_to_html("- item") == "<ul><li>item</li></ul>"

def test_unordered_list_multiple_items():
    # Consecutive dash lines share a single <ul> wrapper.
    assert markdown_to_html("- item 1\n- item 2") == "<ul><li>item 1</li><li>item 2</li></ul>"

def test_unordered_list_blank_line_ends_list():
    # A blank line ends a list.
    assert markdown_to_html("- item 1\n\n- item 2") == "<ul><li>item 1</li></ul>\n<ul><li>item 2</li></ul>"

def test_non_dash_line_closes_list():
    # A non-dash line immediately after a list closes the list.
    assert markdown_to_html("- item\nitem 2") == "<ul><li>item</li></ul>\n<p>item 2</p>"

def test_dash_not_followed_by_space():
    # A dash not followed by a space is not a list item.
    assert markdown_to_html("-No space") == "<p>-No space</p>"

def test_inline_emphasis_in_list_items():
    # Inline emphasis renders inside list items.
    assert markdown_to_html("- _italic item_") == "<ul><li><em>italic item</em></li></ul>"

def test_near_miss_inline_markup_in_list_items():
    # Near-miss inline markup renders as plain text.
    assert markdown_to_html("- *italic item*") == "<ul><li>*italic item*</li></ul>"