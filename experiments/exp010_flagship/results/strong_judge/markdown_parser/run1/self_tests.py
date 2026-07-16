from solution import render_markdown

def test_empty_input_produces_empty_result():
    # An empty input should yield no HTML
    assert render_markdown("") == ""

def test_plain_text_renders_as_paragraph():
    # A line of plain text should render as a paragraph
    assert render_markdown("text") == "<p>text</p>"

def test_non_blank_lines_yield_blocks():
    # Each non-blank line should yield exactly one block
    input_data = "line 1\nline 2\nline 3"
    expected_output = "<p>line 1</p>\n<p>line 2</p>\n<p>line 3</p>"
    assert render_markdown(input_data) == expected_output

def test_blank_lines_emit_nothing():
    # Blank lines should not create empty paragraphs
    input_data = "line 1\n\nline 2"
    expected_output = "<p>line 1</p>\n<p>line 2</p>"
    assert render_markdown(input_data) == expected_output

def test_double_asterisks_render_as_strong():
    # Double asterisks should render as strong emphasis
    assert render_markdown("**bold**") == "<p><strong>bold</strong></p>"

def test_single_underscores_render_as_em():
    # Single underscores should render as emphasis
    assert render_markdown("_italic_") == "<p><em>italic</em></p>"

def test_nested_bold_and_italic():
    # Nested bold and italic should render correctly
    assert render_markdown("**bold _italic_**") == "<p><strong>bold <em>italic</em></strong></p>"

def test_inline_markup_leaves_plain_text_untouched():
    # Inline markup should render in place
    assert render_markdown("text **bold** text") == "<p>text <strong>bold</strong> text</p>"

def test_hashes_followed_by_space_render_as_headings():
    # Hashes followed by a space should render as headings
    assert render_markdown("# Heading 1") == "<h1>Heading 1</h1>"
    assert render_markdown("## Heading 2") == "<h2>Heading 2</h2>"
    assert render_markdown("### Heading 3") == "<h3>Heading 3</h3>"
    assert render_markdown("#### Heading 4") == "<h4>Heading 4</h4>"
    assert render_markdown("##### Heading 5") == "<h5>Heading 5</h5>"
    assert render_markdown("###### Heading 6") == "<h6>Heading 6</h6>"

def test_hash_not_followed_by_space_is_not_heading():
    # A hash not followed by a space is not a heading
    assert render_markdown("#No space") == "<p>#No space</p>"

def test_seven_or_more_hashes_do_not_form_heading():
    # Seven or more hashes should render as a paragraph
    assert render_markdown("####### Too many hashes") == "<p>####### Too many hashes</p>"

def test_inline_emphasis_in_headings():
    # Inline emphasis should render inside heading content
    assert render_markdown("# This is **bold** heading") == "<h1>This is <strong>bold</strong> heading</h1>"

def test_link_markup_renders_as_anchor():
    # Link markup should render as an anchor
    assert render_markdown("[text](url)") == "<p><a href=\"url\">text</a></p>"

def test_link_renders_in_place():
    # Links should render in place within surrounding text
    assert render_markdown("This is a [link](http://example.com) in text.") == "<p>This is a <a href=\"http://example.com\">link</a> in text.</p>"

def test_underscores_in_link_url_not_emphasis():
    # Underscores in link URLs should not be treated as emphasis markers
    assert render_markdown("[text](url_with_underscores)") == "<p><a href=\"url_with_underscores\">text</a></p>"

def test_inline_emphasis_in_links():
    # Inline emphasis should render inside link text
    assert render_markdown("[**bold link**](url)") == "<p><a href=\"url\"><strong>bold link</strong></a></p>"

def test_dash_marked_lists_render_as_unordered_lists():
    # A dash followed by a space should render as list items
    assert render_markdown("- item 1") == "<ul><li>item 1</li></ul>"

def test_consecutive_dash_lines_share_ul_wrapper():
    # Consecutive dash lines should share a single <ul> wrapper
    input_data = "- item 1\n- item 2"
    expected_output = "<ul><li>item 1</li><li>item 2</li></ul>"
    assert render_markdown(input_data) == expected_output

def test_blank_line_ends_list():
    # A blank line should end a list
    input_data = "- item 1\n\n- item 2"
    expected_output = "<ul><li>item 1</li></ul>\n<ul><li>item 2</li></ul>"
    assert render_markdown(input_data) == expected_output

def test_later_dash_starts_new_list():
    # A later dash line should start a new list
    input_data = "- item 1\n\n- item 2"
    expected_output = "<ul><li>item 1</li></ul>\n<ul><li>item 2</li></ul>"
    assert render_markdown(input_data) == expected_output

def test_dash_not_followed_by_space_is_not_a_list_item():
    # A dash not followed by a space should render as a paragraph
    assert render_markdown("-No space") == "<p>-No space</p>"

def test_inline_emphasis_in_list_items():
    # Inline emphasis should render inside list items
    assert render_markdown("- This is **bold** item") == "<ul><li>This is <strong>bold</strong> item</li></ul>"

def test_non_dash_line_closes_list():
    # A non-dash line immediately after a list should close the list
    input_data = "- item 1\n- item 2\ntext"
    expected_output = "<ul><li>item 1</li><li>item 2</li></ul>\n<p>text</p>"
    assert render_markdown(input_data) == expected_output