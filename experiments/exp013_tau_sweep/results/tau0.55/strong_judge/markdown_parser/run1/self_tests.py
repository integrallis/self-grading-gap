from solution import *

def test_empty_input():
    # AC-1.1: Empty input produces an empty result — no HTML at all.
    assert render_markdown("") == ""

def test_plain_text_paragraph():
    # AC-1.2: A line of plain text renders as a paragraph: <p>text</p>.
    assert render_markdown("text") == "<p>text</p>"

def test_multiple_lines_to_blocks():
    # AC-1.3: Each non-blank line yields exactly one block, and the blocks are joined by newlines.
    assert render_markdown("line 1\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_blank_lines_emit_nothing():
    # AC-1.4: Blank lines emit nothing: no empty paragraphs appear in the output.
    assert render_markdown("line 1\n\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_bold_text():
    # AC-2.1: A span wrapped in double asterisks renders as strong emphasis inside its block.
    assert render_markdown("**bold**") == "<p><strong>bold</strong></p>"

def test_italic_text():
    # AC-2.2: A span wrapped in single underscores renders as emphasis inside its block.
    assert render_markdown("_italic_") == "<p><em>italic</em></p>"

def test_nested_emphasis():
    # AC-2.3: The two nest: a bold span wrapping an italic span renders as <strong><em>...</em></strong>.
    assert render_markdown("**_bold and italic_**") == "<p><strong><em>bold and italic</em></strong></p>"

def test_inline_emphasis():
    # AC-2.4: Inline markup renders in place, leaving surrounding plain text untouched on either side.
    assert render_markdown("This is **bold** text.") == "<p>This is <strong>bold</strong> text.</p>"

def test_headings():
    # AC-3.1: A line opening with one to six hashes followed by a space renders as <h1> through <h6>.
    assert render_markdown("# Heading 1") == "<h1>Heading 1</h1>"
    assert render_markdown("## Heading 2") == "<h2>Heading 2</h2>"
    assert render_markdown("### Heading 3") == "<h3>Heading 3</h3>"
    assert render_markdown("#### Heading 4") == "<h4>Heading 4</h4>"
    assert render_markdown("##### Heading 5") == "<h5>Heading 5</h5>"
    assert render_markdown("###### Heading 6") == "<h6>Heading 6</h6>"

def test_no_space_after_hashes():
    # AC-3.2: A hash not followed by a space is not a heading.
    assert render_markdown("#No space") == "<p>#No space</p>"

def test_too_many_hashes():
    # AC-3.3: Seven or more hashes do not form a heading; the line renders as an ordinary paragraph.
    assert render_markdown("####### Too many hashes") == "<p>####### Too many hashes</p>"

def test_inline_emphasis_in_headings():
    # AC-3.4: Inline emphasis renders inside heading content.
    assert render_markdown("## This is **bold**") == "<h2>This is <strong>bold</strong></h2>"

def test_links():
    # AC-4.1: Link markup of the form [text](url) renders as an anchor.
    assert render_markdown("[link](http://example.com)") == "<p><a href=\"http://example.com\">link</a></p>"

def test_link_in_place():
    # AC-4.2: A link renders in place within its surrounding text.
    assert render_markdown("This is a [link](http://example.com).") == "<p>This is a <a href=\"http://example.com\">link</a>.</p>"

def test_underscores_in_link_url():
    # AC-4.3: Underscores inside a link URL are not emphasis markers.
    assert render_markdown("[link_with_underscores](http://example.com/test_page)") == "<p><a href=\"http://example.com/test_page\">link<em>with</em>underscores</a></p>"

def test_inline_emphasis_in_links():
    # AC-4.4: Inline emphasis renders inside the link text, within the anchor.
    assert render_markdown("This is a [_link_](http://example.com).") == "<p>This is a <a href=\"http://example.com\"><em>link</em></a>.</p>"

def test_unordered_lists():
    # AC-5.1: A line of a dash and a space followed by text becomes a one-item unordered list.
    assert render_markdown("- item 1") == "<ul><li>item 1</li></ul>"

def test_multiple_list_items():
    # AC-5.2: Consecutive dash lines share a single <ul> wrapper.
    assert render_markdown("- item 1\n- item 2") == "<ul><li>item 1</li><li>item 2</li></ul>"

def test_blank_line_ends_list():
    # AC-5.3: A blank line ends a list.
    assert render_markdown("- item 1\n\n- item 2") == "<ul><li>item 1</li></ul>\n<ul><li>item 2</li></ul>"

def test_non_dash_line_ends_list():
    # AC-5.6: A non-dash line immediately after a list closes the list and renders as its own block.
    assert render_markdown("- item 1\ntext after list") == "<ul><li>item 1</li></ul>\n<p>text after list</p>"

def test_non_list_dash():
    # AC-5.4: A dash not followed by a space is not a list item.
    assert render_markdown("-item not a list") == "<p>-item not a list</p>"

def test_inline_emphasis_in_list_items():
    # AC-5.5: Inline emphasis renders inside list items.
    assert render_markdown("- **bold item**") == "<ul><li><strong>bold item</strong></li></ul>"

def test_near_miss_fallback():
    # Near-miss markup fallback: unmatched emphasis delimiters render as plain text.
    assert render_markdown("**unclosed") == "<p>**unclosed</p>"