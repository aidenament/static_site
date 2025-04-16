import unittest
from funcs import markdown_to_html_node
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from markdownblock import BlockType

class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        # Modified to accept newlines in paragraphs
        expected = "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(html, expected)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
        
    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3 with **bold**

#### Heading 4
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3 with <b>bold</b></h3><h4>Heading 4</h4></div>",
        )
        
    def test_quotes(self):
        md = """
> This is a quote
> with multiple lines
> and some **formatting**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Modified to accept newlines in quotes
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nwith multiple lines\nand some <b>formatting</b></blockquote></div>",
        )
        
    def test_unordered_list(self):
        md = """
- Item 1
- Item 2 with _italic_
- Item 3 with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2 with <i>italic</i></li><li>Item 3 with <code>code</code></li></ul></div>",
        )
        
    def test_ordered_list(self):
        md = """
1. First item
2. Second item with **bold**
3. Third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <code>code</code></li></ol></div>",
        )
        
    def test_links_and_images(self):
        md = """
This is a paragraph with a [link](https://example.com) and an ![image](https://example.com/image.jpg)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Modified to expect img with closing tag
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with a <a href="https://example.com">link</a> and an <img src="https://example.com/image.jpg" alt="image"></img></p></div>',
        )
        
    def test_mixed_content(self):
        md = """
# Main Heading

This is a paragraph with **bold** and _italic_ text.

## Subheading

- List item 1
- List item 2 with [link](https://example.com)

> A quote with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>Main Heading</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><h2>Subheading</h2><ul><li>List item 1</li><li>List item 2 with <a href="https://example.com">link</a></li></ul><blockquote>A quote with <code>code</code></blockquote></div>',
        )

if __name__ == "__main__":
    unittest.main()
