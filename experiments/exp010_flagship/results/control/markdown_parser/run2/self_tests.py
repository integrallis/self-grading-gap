from solution import render_markdown

def test_empty_input():
    # An empty input should produce an empty result.
    assert render_markdown("") == ""

def test_plain_text_paragraph():
    # A line of plain text renders as a paragraph.
    assert render_markdown("text") == "<p>text</p>"

def test_multiple_lines_paragraphs():
    # Each non-blank line yields exactly one block, joined by newlines.
    assert render_markdown("line 1\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_blank_lines_are_ignored():
    # Blank lines emit nothing; no empty paragraphs should appear.
    assert render_markdown("line 1\n\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_bold_text():
    # A span wrapped in double asterisks renders as strong emphasis.
    assert render_markdown("**bold**") == "<p><strong>bold</strong></p>"

def test_italic_text():
    # A span wrapped in single underscores renders as emphasis.
    assert render_markdown("_italic_") == "<p><em>italic</em></p>"

def test_nested_bold_and_italic():
    # Bold wrapping an italic span renders correctly.
    assert render_markdown("**bold _italic_**") == "<p><strong>bold <em>italic</em></strong></p>"

def test_inline_bold_and_italic():
    # Inline markup renders in place, leaving surrounding text untouched.
    assert render_markdown("This is **bold** and _italic_.") == "<p>This is <strong>bold</strong> and <em>italic</em>.</p>"

def test_headings():
    # A line opening with hashes followed by a space renders as a heading.
    assert render_markdown("# Heading 1") == "<h1>Heading 1</h1>"
    assert render_markdown("## Heading 2") == "<h2>Heading 2</h2>"
    assert render_markdown("### Heading 3") == "<h3>Heading 3</h3>"
    assert render_markdown("#### Heading 4") == "<h4>Heading 4</h4>"
    assert render_markdown("##### Heading 5") == "<h5>Heading 5</h5>"
    assert render_markdown("###### Heading 6") == "<h6>Heading 6</h6>"

def test_heading_no_space():
    # A hash not followed by a space is not a heading.
    assert render_markdown("#No space") == "<p>#No space</p>"

def test_too_many_hashes():
    # Seven or more hashes do not form a heading.
    assert render_markdown("####### Heading") == "<p>####### Heading</p>"

def test_inline_emphasis_in_headings():
    # Inline emphasis renders inside heading content.
    assert render_markdown("## This is **bold**") == "<h2>This is <strong>bold</strong></h2>"

def test_link_rendering():
    # Link markup renders as an anchor.
    assert render_markdown("[text](http://example.com)") == "<p><a href=\"http://example.com\">text</a></p>"

def test_link_in_place():
    # A link renders in place within its surrounding text.
    assert render_markdown("This is a [link](http://example.com).") == "<p>This is a <a href=\"http://example.com\">link</a>.</p>"

def test_link_url_with_underscores():
    # Underscores inside a link URL are not emphasis markers.
    assert render_markdown("[link_with_underscores](http://example_with_underscores.com)") == "<p><a href=\"http://example_with_underscores.com\">link_with_underscores</a></p>"

def test_inline_emphasis_in_links():
    # Inline emphasis renders inside the link text.
    assert render_markdown("[This is **bold**](http://example.com)") == "<p><a href=\"http://example.com\">This is <strong>bold</strong></a></p>"

def test_unordered_list_single_item():
    # A line of a dash and a space becomes a one-item unordered list.
    assert render_markdown("- item") == "<ul><li>item</li></ul>"

def test_unordered_list_multiple_items():
    # Consecutive dash lines share a single <ul> wrapper.
    assert render_markdown("- item 1\n- item 2") == "<ul><li>item 1</li><li>item 2</li></ul>"

def test_blank_line_ends_list():
    # A blank line ends a list.
    assert render_markdown("- item 1\n\n- item 2") == "<ul><li>item 1</li></ul>\n<ul><li>item 2</li></ul>"

def test_non_dash_line_after_list_closes_list():
    # A non-dash line immediately after a list closes the list.
    assert render_markdown("- item 1\ntext") == "<ul><li>item 1</li></ul>\n<p>text</p>"

def test_dash_not_followed_by_space():
    # A dash not followed by a space is not a list item.
    assert render_markdown("-item") == "<p>-item</p>"

def test_inline_emphasis_in_list_items():
    # Inline emphasis renders inside list items.
    assert render_markdown("- This is **bold**") == "<ul><li>This is <strong>bold</strong></li></ul>"