from solution import render_markdown

def test_empty_input():
    # Empty input should produce an empty result
    assert render_markdown('') == ''

def test_plain_text_paragraph():
    # A line of plain text should render as a paragraph
    assert render_markdown('text') == '<p>text</p>'

def test_non_blank_lines_yield_blocks():
    # Each non-blank line yields exactly one block
    assert render_markdown('line 1\nline 2') == '<p>line 1</p>\n<p>line 2</p>'

def test_blank_lines_emit_nothing():
    # Blank lines should not produce empty paragraphs
    assert render_markdown('line 1\n\nline 2') == '<p>line 1</p>\n<p>line 2</p>'

def test_bold_text():
    # Bold text should render with strong tags
    assert render_markdown('**bold**') == '<p><strong>bold</strong></p>'

def test_italic_text():
    # Italic text should render with em tags
    assert render_markdown('_italic_') == '<p><em>italic</em></p>'

def test_nested_bold_and_italic():
    # Nested bold and italic should render correctly
    assert render_markdown('**bold _italic_**') == '<p><strong>bold <em>italic</em></strong></p>'

def test_inline_markup_with_surrounding_text():
    # Inline markup should leave surrounding text untouched
    assert render_markdown('This is **bold** text.') == '<p>This is <strong>bold</strong> text.</p>'

def test_heading_level_1():
    # Heading with one hash should render as <h1>
    assert render_markdown('# Heading 1') == '<h1>Heading 1</h1>'

def test_heading_level_2():
    # Heading with two hashes should render as <h2>
    assert render_markdown('## Heading 2') == '<h2>Heading 2</h2>'

def test_heading_level_3():
    # Heading with three hashes should render as <h3>
    assert render_markdown('### Heading 3') == '<h3>Heading 3</h3>'

def test_heading_level_4():
    # Heading with four hashes should render as <h4>
    assert render_markdown('#### Heading 4') == '<h4>Heading 4</h4>'

def test_heading_level_5():
    # Heading with five hashes should render as <h5>
    assert render_markdown('##### Heading 5') == '<h5>Heading 5</h5>'

def test_heading_level_6():
    # Heading with six hashes should render as <h6>
    assert render_markdown('###### Heading 6') == '<h6>Heading 6</h6>'

def test_heading_with_inline_markup():
    # Headings should support inline markup
    assert render_markdown('### **Bold Heading**') == '<h3><strong>Bold Heading</strong></h3>'

def test_heading_no_space():
    # Hash not followed by a space should render as a paragraph
    assert render_markdown('#No space') == '<p>#No space</p>'

def test_heading_too_many_hashes():
    # Seven or more hashes should render as a paragraph
    assert render_markdown('####### Heading') == '<p>####### Heading</p>'

def test_link_rendering():
    # Link should render as an anchor tag
    assert render_markdown('[text](http://example.com)') == '<p><a href="http://example.com">text</a></p>'

def test_link_with_inline_markup():
    # Links should support inline markup
    assert render_markdown('This is a [**bold** link](http://example.com)') == '<p>This is a <a href="http://example.com"><strong>bold</strong> link</a></p>'

def test_underscore_in_link_url():
    # Underscores in the URL should not be treated as emphasis
    assert render_markdown('[text](http://example.com/test_value)') == '<p><a href="http://example.com/test_value">text</a></p>'

def test_dash_list_item():
    # Dash followed by a space should render as a list item
    assert render_markdown('- item 1') == '<ul><li>item 1</li></ul>'

def test_consecutive_dash_lines():
    # Consecutive dash lines should share a single <ul> wrapper
    assert render_markdown('- item 1\n- item 2') == '<ul><li>item 1</li><li>item 2</li></ul>'

def test_blank_line_ends_list():
    # A blank line should end a list
    assert render_markdown('- item 1\n\n- item 2') == '<ul><li>item 1</li></ul>\n<ul><li>item 2</li></ul>'

def test_dash_not_followed_by_space():
    # Dash not followed by a space should render as a paragraph
    assert render_markdown('-No space') == '<p>-No space</p>'

def test_inline_emphasis_in_list_items():
    # Inline emphasis should work inside list items
    assert render_markdown('- **bold item**') == '<ul><li><strong>bold item</strong></li></ul>'

def test_non_dash_line_after_list_closes_list():
    # A non-dash line should close the list and render as its own block
    assert render_markdown('- item 1\nitem 2') == '<ul><li>item 1</li></ul>\n<p>item 2</p>'