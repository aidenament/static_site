import unittest
from enum import Enum

from textnode import TextNode, TextType
from htmlnode import LeafNode
from funcs import *

class TestFuncs(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)
    
    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")
    
    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")
    
    def test_code(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)
        self.assertEqual(html_node.to_html(), "<code>Code snippet</code>")
    
    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertIsNone(html_node.children)
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Click here</a>')
    
    def test_image(self):
        node = TextNode("Image description", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIsNone(html_node.children)
        self.assertEqual(html_node.props, {"src": "image.jpg", "alt": "Image description"})
        self.assertEqual(html_node.to_html(), '<img src="image.jpg" alt="Image description"></img>')
    
    def test_missing_url_for_link(self):
        node = TextNode("Link without URL", TextType.LINK, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"href": None})
    
    def test_missing_url_for_image(self):
        node = TextNode("Image without URL", TextType.IMAGE, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"src": None, "alt": "Image without URL"})
    
    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        
    def test_special_characters(self):
        node = TextNode("<script>alert('XSS')</script>", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "<script>alert('XSS')</script>")
    
    def test_unsupported_text_type(self):
        # Using a custom class to simulate an unsupported text type
        class MockTextType:
            def __init__(self, value):
                self.value = value
                
        with self.assertRaises(ValueError):
            node = TextNode("Text", MockTextType("unsupported"))
            text_node_to_html_node(node)
    
    # Tests for split_nodes_delimiter function
    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_split_bold_delimiter(self):
        node = TextNode("This text has **bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This text has ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " words")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_split_italic_delimiter(self):
        node = TextNode("This text has *italic* words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This text has ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " words")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_multiple_delimiters(self):
        node = TextNode("Text with `code` and more `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and more ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
    
    def test_delimiter_at_start(self):
        node = TextNode("`code` at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)  # Now expecting 3 nodes instead of 2
        self.assertEqual(new_nodes[0].text, "code")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " at the beginning")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
    
    def test_delimiter_at_end(self):
        node = TextNode("end with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "end with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
    
    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 0) 
    
    def test_text_without_delimiter(self):
        node = TextNode("This text has no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This text has no delimiters")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_only_delimiters(self):
        node = TextNode("`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
    
    def test_consecutive_delimiters(self):
        node = TextNode("Text``Double", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "")  # Empty text node with CODE type
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, "Double")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_non_text_nodes_unchanged(self):
        bold_node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([bold_node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], bold_node)
    
    def test_mixed_nodes(self):
        text_node = TextNode("Text with `code`", TextType.TEXT)
        bold_node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([text_node, bold_node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2], bold_node)
    
    def test_complex_delimiter(self):
        node = TextNode("Check this [link](https://example.com)[link] here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "[link]", TextType.LINK)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Check this ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "(https://example.com)")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[2].text, " here")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_empty_delimiter(self):
        node = TextNode("This should not split", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "", TextType.CODE)
        self.assertEqual(str(context.exception), "delimiter cannot be empty string")
    
    def test_none_delimiter(self):
        node = TextNode("This should not split", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], None, TextType.CODE)
        self.assertEqual(str(context.exception), "delimeter cannot be None")
    
    def test_empty_nodes_list(self):
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 0)
    
    # Tests for extract_markdown_images function
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(list(matches), [("image", "https://i.imgur.com/zjjcJKZ.png")])
    
    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "Here are multiple images: ![first](image1.jpg) and ![second](image2.png)"
        )
        self.assertEqual(
            list(matches), 
            [("first", "image1.jpg"), ("second", "image2.png")]
        )
    
    def test_extract_mixed_links_and_images(self):
        matches = extract_markdown_images(
            "Image: ![alt text](image.jpg) and link: [link text](https://example.com)"
        )
        self.assertEqual(list(matches), [("alt text", "image.jpg"), ("link text", "https://example.com")])
    
    def test_extract_no_images(self):
        matches = extract_markdown_images("This text has no markdown images or links")
        self.assertEqual(list(matches), [])
    
    def test_empty_input(self):
        matches = extract_markdown_images("")
        self.assertEqual(list(matches), [])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    # Additional tests for split_nodes_images
    def test_split_nodes_images_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertEqual(len(new_nodes), 0)
    
    def test_split_nodes_images_no_images(self):
        node = TextNode("This text has no images", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This text has no images")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_split_nodes_images_image_at_start(self):
        node = TextNode("![first image](image1.jpg) followed by text", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "first image", "First node should be the image alt text")
        self.assertEqual(new_nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[0].url, "image1.jpg")
        self.assertEqual(new_nodes[1].text, " followed by text")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
    
    def test_split_nodes_images_image_at_end(self):
        node = TextNode("Text followed by ![last image](image2.jpg)", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Text followed by ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "last image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "image2.jpg")
    
    def test_split_nodes_images_multiple_nodes(self):
        node1 = TextNode("First with ![image1](url1.jpg)", TextType.TEXT)
        node2 = TextNode("Second with ![image2](url2.jpg)", TextType.TEXT)
        new_nodes = split_nodes_images([node1, node2])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "First with ")
        self.assertEqual(new_nodes[1].text, "image1")
        self.assertEqual(new_nodes[1].url, "url1.jpg")
        self.assertEqual(new_nodes[2].text, "Second with ")
        self.assertEqual(new_nodes[3].text, "image2")
        self.assertEqual(new_nodes[3].url, "url2.jpg")
    
    def test_split_nodes_images_non_text_nodes(self):
        node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_images([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Bold text")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
    
    # Tests for split_nodes_links function
    def test_split_nodes_links_basic(self):
        node = TextNode("Here's a [link](https://example.com) to click", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Here's a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example.com")
        self.assertEqual(new_nodes[2].text, " to click")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_split_nodes_links_multiple_links(self):
        node = TextNode("Visit [site1](https://example1.com) or [site2](https://example2.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Visit ")
        self.assertEqual(new_nodes[1].text, "site1")
        self.assertEqual(new_nodes[1].url, "https://example1.com")
        self.assertEqual(new_nodes[2].text, " or ")
        self.assertEqual(new_nodes[3].text, "site2")
        self.assertEqual(new_nodes[3].url, "https://example2.com")
    
    def test_split_nodes_links_link_at_start(self):
        node = TextNode("[Start link](https://example.com) followed by text", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Start link")
        self.assertEqual(new_nodes[0].text_type, TextType.LINK)
        self.assertEqual(new_nodes[0].url, "https://example.com")
        self.assertEqual(new_nodes[1].text, " followed by text")
    
    def test_split_nodes_links_link_at_end(self):
        node = TextNode("Text followed by [end link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Text followed by ")
        self.assertEqual(new_nodes[1].text, "end link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example.com")
    
    def test_split_nodes_links_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(len(new_nodes), 0)
    
    def test_split_nodes_links_no_links(self):
        node = TextNode("This text has no links", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This text has no links")
    
    def test_split_nodes_links_non_text_nodes(self):
        node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_links([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
    
    def test_split_nodes_links_with_special_chars(self):
        node = TextNode("Check this [link with spaces](https://example.com/path?query=value&param=2)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[1].text, "link with spaces")
        self.assertEqual(new_nodes[1].url, "https://example.com/path?query=value&param=2")
    
    def test_split_nodes_links_multiple_nodes(self):
        node1 = TextNode("First [link1](url1)", TextType.TEXT)
        node2 = TextNode("Second [link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_links([node1, node2])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "First ")
        self.assertEqual(new_nodes[1].text, "link1")
        self.assertEqual(new_nodes[1].url, "url1")
        self.assertEqual(new_nodes[2].text, "Second ")
        self.assertEqual(new_nodes[3].text, "link2")
        self.assertEqual(new_nodes[3].url, "url2")

    def test_text_to_textnodes_base(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " word and a ")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " and an ")
        self.assertEqual(nodes[6].text_type, TextType.TEXT)
        self.assertEqual(nodes[7].text, "obi wan image")
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(nodes[8].text, " and a ")
        self.assertEqual(nodes[8].text_type, TextType.TEXT)
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].text_type, TextType.LINK)
        self.assertEqual(nodes[9].url, "https://boot.dev")

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type_heading(self):
        # Test heading blocks with different levels
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Test that more than 6 # characters is not a heading
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)
        # Test that # without space is not a heading
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_code(self):
        # Test code blocks
        self.assertEqual(block_to_block_type("```\ncode block\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python\ndef hello():\n    print('Hello')\n```"), BlockType.CODE)
        # Test that backticks without closing is not a code block
        self.assertEqual(block_to_block_type("```\nunclosed code"), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_quote(self):
        # Test quote blocks
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Multi-line\n> quote block"), BlockType.QUOTE)
        # Test that text without > at start is not a quote
        self.assertEqual(block_to_block_type("Not a > quote"), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_unordered_list(self):
        # Test unordered lists
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        # Test that text without - at start is not an unordered list
        self.assertEqual(block_to_block_type("Item 1"), BlockType.PARAGRAPH)
        # Test that - without space is not an unordered list
        self.assertEqual(block_to_block_type("-No space"), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_ordered_list(self):
        # Test ordered lists
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), BlockType.ORDERED_LIST)
        # Test that text without number + dot + space at start is not an ordered list
        self.assertEqual(block_to_block_type("Item 1"), BlockType.PARAGRAPH)
        # Test that number without dot and space is not an ordered list
        self.assertEqual(block_to_block_type("1Item 1"), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_paragraph(self):
        # Test regular paragraphs
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Multi-line\nparagraph text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Special chars !@#$%^&*()"), BlockType.PARAGRAPH)

    # Tests for extract_title function
    def test_extract_title_basic(self):
        markdown = "# Hello\nThis is content"
        self.assertEqual(extract_title(markdown), "Hello")
    
    def test_extract_title_with_whitespace(self):
        markdown = "#     Title with spaces    \nContent"
        self.assertEqual(extract_title(markdown), "Title with spaces")
    
    def test_extract_title_with_formatting(self):
        markdown = "# Title with **bold** and _italic_\nContent"
        self.assertEqual(extract_title(markdown), "Title with **bold** and _italic_")
    
    def test_extract_title_multi_line(self):
        markdown = "Some text\n# The Title\nMore content"
        self.assertEqual(extract_title(markdown), "The Title")
    
    def test_extract_title_no_h1(self):
        markdown = "No h1 here\n## This is h2"
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")
    
    def test_extract_title_empty_markdown(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()
