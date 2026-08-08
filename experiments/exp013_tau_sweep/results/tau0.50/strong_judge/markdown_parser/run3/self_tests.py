from solution import markdown_to_html

def test_empty_input_produces_empty_result():
    # An empty input should yield no HTML.
    assert markdown_to_html("") == ""

def test_plain_text_renders_as_paragraph():
    # A line of plain text should render as a paragraph.
    assert markdown_to_html("text") == "<p>text</p>"

def test_non_blank_lines_yield_blocks():
    # Each non-blank line should yield one block, joined by newlines.
    input_text = "line1\nline2\nline3"
    expected_output = "<p>line1</p>\n<p>line2</p>\n<p>line3</p>"
    assert markdown_to_html(input_text) == expected_output

def test_blank_lines_emit_nothing():
    # Blank lines should not produce empty paragraphs.
    input_text = "text\n\nmore text"
    expected_output = "<p>text</p>\n<p>more text</p>"
    assert markdown_to_html(input_text) == expected_output

def test_bold_renders_as_strong():
    # A span wrapped in double asterisks should render as strong emphasis.
    assert markdown_to_html("**bold**") == "<p><strong>bold</strong></p>"

def test_italic_renders_as_em():
    # A span wrapped in single underscores should render as emphasis.
    assert markdown_to_html("_italic_") == "<p><em>italic</em></p>"

def test_nested_bold_and_italic():
    # Bold wrapping an italic span should render with both tags.
    assert markdown_to_html("**bold _italic_**") == "<p><strong>bold <em>italic</em></strong></p>"

def test_inline_markup_renders_in_place():
    # Inline markup should render in place.
    assert markdown_to_html("This is **bold** text.") == "<p>This is <strong>bold</strong> text.</p>"
    assert markdown_to_html("This is _italic_ text.") == "<p>This is <em>italic</em> text.</p>"

def test_heading_rendering():
    # A line with hashes followed by a space should render as a heading.
    assert markdown_to_html("# Heading 1") == "<h1>Heading 1</h1>"
    assert markdown_to_html("## Heading 2") == "<h2>Heading 2</h2>"
    assert markdown_to_html("### Heading 3") == "<h3>Heading 3</h3>"
    assert markdown_to_html("#### Heading 4") == "<h4>Heading 4</h4>"
    assert markdown_to_html("##### Heading 5") == "<h5>Heading 5</h5>"
    assert markdown_to_html("###### Heading 6") == "<h6>Heading 6</h6>"

def test_no_space_after_hash_is_paragraph():
    # A hash not followed by a space is not a heading.
    assert markdown_to_html("#No space") == "<p>#No space</p>"

def test_seven_or_more_hashes_not_heading():
    # Seven or more hashes do not form a heading.
    assert markdown_to_html("####### Too many hashes") == "<p>####### Too many hashes</p>"

def test_inline_emphasis_in_headings():
    # Inline emphasis should render inside heading content.
    assert markdown_to_html("### **Bold Heading**") == "<h3><strong>Bold Heading</strong></h3>"
    assert markdown_to_html("### _Italic Heading_") == "<h3><em>Italic Heading</em></h3>"

def test_link_renders_as_anchor():
    # Link markup should render as an anchor.
    assert markdown_to_html("[text](url)") == "<p><a href=\"url\">text</a></p>"

def test_link_renders_in_place():
    # A link should render in place within surrounding text.
    assert markdown_to_html("This is a [link](http://example.com).") == "<p>This is a <a href=\"http://example.com\">link</a>.</p>"

def test_underscores_in_link_url():
    # Underscores inside a link URL should not alter the URL.
    assert markdown_to_html("[link_with_underscores](http://example.com/some_page)") == "<p><a href=\"http://example.com/some_page\">link<em>with</em>underscores</a></p>"

def test_link_with_no_underscores():
    # A link with label containing no underscores should render correctly.
    assert markdown_to_html("[label](http://example.com/some_page)") == "<p><a href=\"http://example.com/some_page\">label</a></p>"

def test_inline_emphasis_in_links():
    # Inline emphasis should render inside the link text.
    assert markdown_to_html("[**bold link**](url)") == "<p><a href=\"url\"><strong>bold link</strong></a></p>"
    assert markdown_to_html("[_italic link_](url)") == "<p><a href=\"url\"><em>italic link</em></a></p>"

def test_unordered_list_single_item():
    # A line starting with dash and space should become a list item.
    assert markdown_to_html("- item") == "<ul><li>item</li></ul>"

def test_consecutive_dash_lines_share_ul_wrapper():
    # Consecutive dash lines should share a <ul> wrapper.
    input_text = "- item 1\n- item 2"
    expected_output = "<ul><li>item 1</li><li>item 2</li></ul>"
    assert markdown_to_html(input_text) == expected_output

def test_blank_line_ends_list():
    # A blank line ends a list.
    input_text = "- item 1\n\n- item 2"
    expected_output = "<ul><li>item 1</li></ul>\n<ul><li>item 2</li></ul>"
    assert markdown_to_html(input_text) == expected_output

def test_non_dash_line_after_list_closes_list():
    # A non-dash line immediately after a list closes the list.
    input_text = "- item 1\ntext"
    expected_output = "<ul><li>item 1</li></ul>\n<p>text</p>"
    assert markdown_to_html(input_text) == expected_output

def test_dash_not_followed_by_space_is_paragraph():
    # A dash not followed by a space should render as a paragraph.
    assert markdown_to_html("-No space") == "<p>-No space</p>"

def test_inline_emphasis_in_list_items():
    # Inline emphasis should render inside list items.
    assert markdown_to_html("- **bold item**") == "<ul><li><strong>bold item</strong></li></ul>"
    assert markdown_to_html("- _italic item_") == "<ul><li><em>italic item</em></li></ul>"

def test_near_miss_markup_fallback():
    # Unclosed emphasis should render as plain text.
    assert markdown_to_html("**unclosed") == "<p>**unclosed</p>"