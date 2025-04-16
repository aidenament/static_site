import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_mismatch(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_empty_node(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, TextType.TEXT)
    
    def test_url_equality(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)
    
    def test_url_inequality(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("Sample text", TextType.BOLD, None)
        expected = "TextNode(Sample text, bold, None)"
        self.assertEqual(repr(node), expected)
    
    def test_repr_with_url(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        expected = "TextNode(Link text, link, https://example.com)"
        self.assertEqual(repr(node), expected)
        
    def test_image_node(self):
        node = TextNode("Image alt text", TextType.IMAGE, "image.jpg")
        self.assertEqual(node.text, "Image alt text")
        self.assertEqual(node.text_type, TextType.IMAGE)
        self.assertEqual(node.url, "image.jpg")
    
    def test_default_url(self):
        node = TextNode("Regular text", TextType.TEXT)
        self.assertIsNone(node.url)
        


if __name__ == "__main__":
    unittest.main()
