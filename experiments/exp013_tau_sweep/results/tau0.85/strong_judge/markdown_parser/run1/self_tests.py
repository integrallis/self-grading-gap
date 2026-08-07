# your complete test file
from solution import *

def test_empty_input():
    # An empty input produces an empty result.
    assert render_markdown("") == ""

def test_single_plain_line():
    # A line of plain text renders as a paragraph: <p>text</p>.
    assert render_markdown("text") == "<p>text</p>"

def test_multiple_plain_lines():
    # Each non-blank line yields exactly one block, and the blocks are joined by newlines.
    assert render_markdown("line 1\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_blank_lines():
    # Blank lines emit nothing: no empty paragraphs appear in the output.
    assert render_markdown("line 1\n\nline 2") == "<p>line 1</p>\n<p>line 2</p>"

def test_blank_only_input():
    # Blank-only input emits no HTML.
    assert render_markdown("\n") == ""

def test_single_bold():
    # A span wrapped in double asterisks renders as strong emphasis inside its block.
    assert render_markdown("**bold**") == "<p><strong>bold</strong></p>"

def test_single_italic():
    # A span wrapped in single underscores renders as emphasis inside its block.
    assert render_markdown("_italic_") == "<p><em>italic</em></p>"

def test_nested_bold_italic():
    # A bold span wrapping an italic span renders as <strong><em>...</em></strong>.
    assert render_markdown("**bold _italic_**") == "<p><strong>bold <em>italic</em></strong></p>"

def test_inline_markup():
    # Inline markup renders in place, leaving surrounding plain text untouched on either side.
    assert render_markdown("This is **bold** and _italic_.") == "<p>This is <strong>bold</strong> and <em>italic</em>.</p>"

def test_headings():
    assert render_markdown("# Heading 1") == "<h1>Heading 1</h1>"
    assert render_markdown("## Heading 2") == "<h2>Heading 2</h2>"
    assert render_markdown("### Heading 3") == "<h3>Heading 3</h3>"
    assert render_markdown("#### Heading 4") == "<h4>Heading 4</h4>"
    assert render_markdown("##### Heading 5") == "<h5>Heading 5</h5>"
    assert render_markdown("###### Heading 6") == "<h6>Heading 6</h6>"
    assert render_markdown("#No space") == "<p>#No space</p>"
    assert render_markdown("####### Too many hashes") == "<p>####### Too many hashes</p>"
    assert render_markdown("# Heading with **bold** and _italic_") == "<h1>Heading with <strong>bold</strong> and <em>italic</em></h1>"
    assert render_markdown("######## Too many hashes") == "<p>######## Too many hashes</p>"  # eight hashes case

def test_links():
    assert render_markdown("[link](http://example.com)") == "<p><a href=\"http://example.com\">link</a></p>"
    assert render_markdown("This is a [link](http://example.com).") == "<p>This is a <a href=\"http://example.com\">link</a>.</p>"
    assert render_markdown("[link_with_underscores](http://example.com/with_underscores)") == "<p><a href=\"http://example.com/with_underscores\">link<em>with</em>underscores</a></p>"  # link text processed, URL remains unchanged
    assert render_markdown("This is a [**bold link**](http://example.com).") == "<p>This is a <a href=\"http://example.com\"><strong>bold link</strong></a>.</p>"
    assert render_markdown("[_italic_](http://example.com)") == '<p><a href="http://example.com"><em>italic</em></a></p>'  # italic emphasis inside link text

def test_unordered_lists():
    assert render_markdown("- Item 1") == "<ul><li>Item 1</li></ul>"
    assert render_markdown("- Item 1\n- Item 2") == "<ul><li>Item 1</li><li>Item 2</li></ul>"
    assert render_markdown("- Item 1\n\n- Item 2") == "<ul><li>Item 1</li></ul>\n<ul><li>Item 2</li></ul>"
    assert render_markdown("- Item 1\nNot a list") == "<ul><li>Item 1</li></ul>\n<p>Not a list</p>"
    assert render_markdown("- Item 1 is **bold**") == "<ul><li>Item 1 is <strong>bold</strong></li></ul>"
    assert render_markdown("Not a list\n- Item 1") == "<p>Not a list</p>\n<ul><li>Item 1</li></ul>"
    assert render_markdown("- _italic_") == "<ul><li><em>italic</em></li></ul>"  # verify italic emphasis inside list items
    assert render_markdown("-No space") == "<p>-No space</p>"  # dash-without-space case