from solution import *

def test_empty_input():
    # AC-1.1: Empty input produces an empty result — no HTML at all.
    assert render_markdown("") == ""

def test_plain_text():
    # AC-1.2: A line of plain text renders as a paragraph: <p>text</p>.
    assert render_markdown("text") == "<p>text</p>"

def test_multiple_lines_plain_text():
    # AC-1.3: Each non-blank line yields exactly one block, and the blocks are joined by newlines.
    assert render_markdown("line 1\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_blank_line():
    # AC-1.4: Blank lines emit nothing: no empty paragraphs appear in the output.
    assert render_markdown("line 1\n\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_bold_text():
    # AC-2.1: A span wrapped in double asterisks renders as strong emphasis inside its block.
    assert render_markdown("**bold**") == "<p><strong>bold</strong></p>"

def test_italic_text():
    # AC-2.2: A span wrapped in single underscores renders as emphasis inside its block.
    assert render_markdown("_italic_") == "<p><em>italic</em></p>"

def test_nested_bold_and_italic():
    # AC-2.3: The two nest: a bold span wrapping an italic span renders as <strong><em>...</em></strong>.
    assert render_markdown("**bold _italic_**") == "<p><strong>bold <em>italic</em></strong></p>"

def test_inline_markup():
    # AC-2.4: Inline markup renders in place, leaving surrounding plain text untouched on either side.
    assert render_markdown("This is **bold** text.") == "<p>This is <strong>bold</strong> text.</p>"

def test_inline_italic_markup():
    # AC-2.4: Inline markup renders in place, leaving surrounding plain text untouched on either side.
    assert render_markdown("This is _italic_ text.") == "<p>This is <em>italic</em> text.</p>"

def test_headings():
    # AC-3.1: A line opening with one to six hashes followed by a space renders as <h1> through <h6>.
    assert render_markdown("# Heading 1") == "<h1>Heading 1</h1>"
    assert render_markdown("## Heading 2") == "<h2>Heading 2</h2>"
    assert render_markdown("### Heading 3") == "<h3>Heading 3</h3>"
    assert render_markdown("#### Heading 4") == "<h4>Heading 4</h4>"
    assert render_markdown("##### Heading 5") == "<h5>Heading 5</h5>"
    assert render_markdown("###### Heading 6") == "<h6>Heading 6</h6>"

def test_heading_no_space():
    # AC-3.2: A hash not followed by a space is not a heading.
    assert render_markdown("#No space") == "<p>#No space</p>"

def test_heading_too_many_hashes():
    # AC-3.3: Seven or more hashes do not form a heading; the line renders as an ordinary paragraph.
    assert render_markdown("####### Heading") == "<p>####### Heading</p>"

def test_heading_with_inline_markup():
    # AC-3.4: Inline emphasis renders inside heading content.
    assert render_markdown("# This is **bold**") == "<h1>This is <strong>bold</strong></h1>"

def test_heading_with_inline_italic():
    # AC-3.4: Inline emphasis renders inside heading content.
    assert render_markdown("# This is _italic_") == "<h1>This is <em>italic</em></h1>"

def test_link():
    # AC-4.1: Link markup of the form [text](url) renders as an anchor.
    assert render_markdown("[link](http://example.com)") == "<p><a href=\"http://example.com\">link</a></p>"

def test_link_in_place():
    # AC-4.2: A link renders in place within its surrounding text.
    assert render_markdown("This is a [link](http://example.com).") == "<p>This is a <a href=\"http://example.com\">link</a>.</p>"

def test_link_url_with_underscores():
    # AC-4.3: Underscores inside a link URL are not emphasis markers.
    assert render_markdown("[link](http://example_com)") == "<p><a href=\"http://example_com\">link</a></p>"

def test_link_with_inline_emphasis():
    # AC-4.4: Inline emphasis renders inside the link text.
    assert render_markdown("[**bold link**](http://example.com)") == "<p><a href=\"http://example.com\"><strong>bold link</strong></a></p>"

def test_link_with_inline_italic():
    # AC-4.4: Inline emphasis renders inside the link text.
    assert render_markdown("[_italic link_](http://example.com)") == "<p><a href=\"http://example.com\"><em>italic link</em></a></p>"

def test_unordered_list():
    # AC-5.1: A line of a dash and a space followed by text becomes a one-item unordered list.
    assert render_markdown("- item") == "<ul><li>item</li></ul>"

def test_consecutive_unordered_list_items():
    # AC-5.2: Consecutive dash lines share a single <ul> wrapper.
    assert render_markdown("- item 1\n- item 2") == "<ul><li>item 1</li><li>item 2</li></ul>"

def test_blank_line_ends_list():
    # AC-5.3: A blank line ends a list; a later dash line starts a new list of its own.
    assert render_markdown("- item 1\n\n- item 2") == "<ul><li>item 1</li></ul>\n<ul><li>item 2</li></ul>"

def test_non_dash_as_paragraph():
    # AC-5.4: A dash not followed by a space is not a list item.
    assert render_markdown("-item") == "<p>-item</p>"

def test_inline_emphasis_in_list():
    # AC-5.5: Inline emphasis renders inside list items.
    assert render_markdown("- This is **bold** in a list.") == "<ul><li>This is <strong>bold</strong> in a list.</li></ul>"

def test_inline_italic_in_list():
    # AC-5.5: Inline emphasis renders inside list items.
    assert render_markdown("- This is _italic_ in a list.") == "<ul><li>This is <em>italic</em> in a list.</li></ul>"

def test_end_list_with_non_dash():
    # AC-5.6: A non-dash line immediately after a list closes the list and renders as its own block.
    assert render_markdown("- item 1\n- item 2\nThis is a new paragraph.") == "<ul><li>item 1</li><li>item 2</li></ul>\n<p>This is a new paragraph.</p>"

def test_malformed_bold():
    # Near-miss markup falls back to plain text: unclosed bold.
    assert render_markdown("**unclosed") == "<p>**unclosed</p>"

def test_malformed_italic():
    # Near-miss markup falls back to plain text: unclosed italic.
    assert render_markdown("_unclosed") == "<p>_unclosed</p>"

def test_malformed_link():
    # Near-miss markup falls back to plain text: unclosed link.
    assert render_markdown("[text](url") == "<p>[text](url</p>"