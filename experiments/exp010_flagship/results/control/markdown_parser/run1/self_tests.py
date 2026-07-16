from solution import markdown_to_html

def test_empty_input():
    # Empty input produces an empty result
    assert markdown_to_html("") == ""

def test_plain_text_paragraph():
    # A line of plain text renders as a paragraph
    assert markdown_to_html("text") == "<p>text</p>"

def test_multiple_blocks():
    # Each non-blank line yields exactly one block, joined by newlines
    input_text = "line 1\nline 2\nline 3"
    expected_output = "<p>line 1</p>\n<p>line 2</p>\n<p>line 3</p>"
    assert markdown_to_html(input_text) == expected_output

def test_blank_lines():
    # Blank lines emit nothing: no empty paragraphs appear in the output
    input_text = "line 1\n\nline 2"
    expected_output = "<p>line 1</p>\n<p>line 2</p>"
    assert markdown_to_html(input_text) == expected_output

def test_bold_text():
    # A span wrapped in double asterisks renders as strong emphasis
    assert markdown_to_html("**bold**") == "<p><strong>bold</strong></p>"

def test_italic_text():
    # A span wrapped in single underscores renders as emphasis
    assert markdown_to_html("_italic_") == "<p><em>italic</em></p>"

def test_nested_emphasis():
    # A bold span wrapping an italic span renders correctly
    assert markdown_to_html("**bold _italic_**") == "<p><strong><em>italic</em></strong></p>"

def test_inline_markup():
    # Inline markup renders in place, leaving surrounding plain text untouched
    assert markdown_to_html("This is **bold** text") == "<p>This is <strong>bold</strong> text</p>"

def test_heading_level_1():
    # A line opening with one hash followed by a space renders as <h1>
    assert markdown_to_html("# Heading") == "<h1>Heading</h1>"

def test_heading_level_2():
    # A line opening with two hashes followed by a space renders as <h2>
    assert markdown_to_html("## Subheading") == "<h2>Subheading</h2>"

def test_no_space_after_hash():
    # A hash not followed by a space is not a heading
    assert markdown_to_html("#No space") == "<p>#No space</p>"

def test_too_many_hashes():
    # Seven or more hashes do not form a heading
    assert markdown_to_html("####### Too many hashes") == "<p>####### Too many hashes</p>"

def test_heading_with_emphasis():
    # Inline emphasis renders inside heading content
    assert markdown_to_html("# This is **bold**") == "<h1>This is <strong>bold</strong></h1>"

def test_link_rendering():
    # Link markup renders as an anchor
    assert markdown_to_html("[text](url)") == "<p><a href=\"url\">text</a></p>"

def test_link_with_emphasis():
    # Inline emphasis renders inside the link text
    assert markdown_to_html("[This is **bold**](url)") == "<p><a href=\"url\">This is <strong>bold</strong></a></p>"

def test_link_standing_alone():
    # A link standing alone on a line still gets a paragraph wrapper
    assert markdown_to_html("[text](url)") == "<p><a href=\"url\">text</a></p>"

def test_underscore_in_url():
    # Underscores inside a link URL are not emphasis markers
    assert markdown_to_html("[text](url_with_underscore)") == "<p><a href=\"url_with_underscore\">text</a></p>"

def test_unordered_list_item():
    # A line of a dash and a space becomes a one-item unordered list
    assert markdown_to_html("- item") == "<ul><li>item</li></ul>"

def test_consecutive_list_items():
    # Consecutive dash lines share a single <ul> wrapper
    input_text = "- item 1\n- item 2"
    expected_output = "<ul><li>item 1</li><li>item 2</li></ul>"
    assert markdown_to_html(input_text) == expected_output

def test_blank_line_ends_list():
    # A blank line ends a list
    input_text = "- item 1\n\n- item 2"
    expected_output = "<ul><li>item 1</li></ul>\n<p></p>\n<ul><li>item 2</li></ul>"
    assert markdown_to_html(input_text) == expected_output

def test_non_dash_line_ends_list():
    # A non-dash line immediately after a list closes the list
    input_text = "- item 1\nitem 2"
    expected_output = "<ul><li>item 1</li></ul>\n<p>item 2</p>"
    assert markdown_to_html(input_text) == expected_output

def test_dash_not_followed_by_space():
    # A dash not followed by a space is not a list item
    assert markdown_to_html("-No space") == "<p>-No space</p>"

def test_inline_emphasis_in_list():
    # Inline emphasis renders inside list items
    assert markdown_to_html("- This is **bold**") == "<ul><li>This is <strong>bold</strong></li></ul>"