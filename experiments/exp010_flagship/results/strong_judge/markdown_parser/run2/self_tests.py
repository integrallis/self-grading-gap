import solution

def test_empty_input_produces_empty_result():
    # Empty input should produce no HTML at all
    assert solution.render_markdown("") == ""

def test_plain_text_renders_as_paragraph():
    # A line of plain text renders as a paragraph
    assert solution.render_markdown("text") == "<p>text</p>"

def test_non_blank_lines_yield_one_block():
    # Each non-blank line yields exactly one block, joined by newlines
    assert solution.render_markdown("line 1\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_blank_lines_emit_nothing():
    # Blank lines emit nothing
    assert solution.render_markdown("line 1\n\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_double_asterisks_render_as_strong():
    # A span wrapped in double asterisks renders as strong emphasis
    assert solution.render_markdown("This is **bold** text.") == "<p>This is <strong>bold</strong> text.</p>"

def test_single_underscores_render_as_emphasis():
    # A span wrapped in single underscores renders as emphasis
    assert solution.render_markdown("This is _italic_ text.") == "<p>This is <em>italic</em> text.</p>"

def test_nesting_bold_and_italic():
    # Bold span wrapping an italic span renders correctly
    assert solution.render_markdown("This is **_bold and italic_** text.") == "<p>This is <strong><em>bold and italic</em></strong> text.</p>"

def test_inline_markup_leaves_surrounding_text_untouched():
    # Inline markup renders in place with surrounding text untouched
    assert solution.render_markdown("This is **bold** and _italic_ text.") == "<p>This is <strong>bold</strong> and <em>italic</em> text.</p>"

def test_hashes_followed_by_space_render_as_headings():
    # A line with hashes followed by a space renders as a heading
    assert solution.render_markdown("# Heading 1") == "<h1>Heading 1</h1>"
    assert solution.render_markdown("## Heading 2") == "<h2>Heading 2</h2>"
    assert solution.render_markdown("### Heading 3") == "<h3>Heading 3</h3>"
    assert solution.render_markdown("#### Heading 4") == "<h4>Heading 4</h4>"
    assert solution.render_markdown("##### Heading 5") == "<h5>Heading 5</h5>"
    assert solution.render_markdown("###### Heading 6") == "<h6>Heading 6</h6>"

def test_hashes_not_followed_by_space_render_as_paragraph():
    # A hash not followed by a space is not a heading
    assert solution.render_markdown("#No space") == "<p>#No space</p>"

def test_seven_hashes_or_more_render_as_paragraph():
    # Seven or more hashes do not form a heading
    assert solution.render_markdown("####### More than six hashes") == "<p>####### More than six hashes</p>"

def test_inline_emphasis_in_headings():
    # Inline emphasis renders inside heading content
    assert solution.render_markdown("## This is **bold** in a heading") == "<h2>This is <strong>bold</strong> in a heading</h2>"

def test_link_markup_renders_as_anchor():
    # Link markup renders as an anchor
    assert solution.render_markdown("[link text](http://example.com)") == "<p><a href=\"http://example.com\">link text</a></p>"

def test_link_renders_in_place():
    # A link renders in place within surrounding text
    assert solution.render_markdown("This is a [link](http://example.com).") == "<p>This is a <a href=\"http://example.com\">link</a>.</p>"

def test_underscores_in_link_url_do_not_render_as_emphasis():
    # Underscores inside a link URL are not emphasis markers
    assert solution.render_markdown("[link_text](http://example_with_underscores.com)") == "<p><a href=\"http://example_with_underscores.com\">link_text</a></p>"

def test_bold_emphasis_in_link_text():
    # Inline emphasis renders inside the link text
    assert solution.render_markdown("This is a [**bold link**](http://example.com).") == "<p>This is a <a href=\"http://example.com\"><strong>bold link</strong></a>.</p>"

def test_dash_marked_lists_render_as_unordered_lists():
    # A line of a dash and a space followed by text becomes a one-item unordered list
    assert solution.render_markdown("- item") == "<ul><li>item</li></ul>"

def test_consecutive_dash_lines_share_ul_wrapper():
    # Consecutive dash lines share a single <ul> wrapper
    assert solution.render_markdown("- item 1\n- item 2") == "<ul><li>item 1</li><li>item 2</li></ul>"

def test_blank_line_ends_a_list():
    # A blank line ends a list
    assert solution.render_markdown("- item 1\n\n- item 2") == "<ul><li>item 1</li></ul>\n<ul><li>item 2</li></ul>"

def test_dash_line_not_followed_by_space_is_not_item():
    # A dash not followed by a space is not a list item
    assert solution.render_markdown("-item") == "<p>-item</p>"

def test_bold_emphasis_in_list_items():
    # Inline emphasis renders inside list items
    assert solution.render_markdown("- This is **bold** inside a list.") == "<ul><li>This is <strong>bold</strong> inside a list.</li></ul>"

def test_non_dash_line_closes_the_list():
    # A non-dash line immediately after a list closes the list
    assert solution.render_markdown("- item 1\n- item 2\nThis is a new paragraph.") == "<ul><li>item 1</li><li>item 2</li></ul>\n<p>This is a new paragraph.</p>"

def test_inline_emphasis_in_link_text():
    # Inline emphasis renders inside link text
    assert solution.render_markdown("[_italic_](http://example.com)") == "<p><a href=\"http://example.com\"><em>italic</em></a></p>"

def test_italic_emphasis_in_list_items():
    # Inline emphasis renders inside list items
    assert solution.render_markdown("- _italic_ inside a list.") == "<ul><li><em>italic</em> inside a list.</li></ul>"

def test_italic_heading():
    # Italic emphasis in a heading
    assert solution.render_markdown("## _italic_ heading") == "<h2><em>italic</em> heading</h2>"